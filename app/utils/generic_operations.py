from typing import Sequence
from fastapi import Response, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select, update, Connection
from sqlalchemy.ext.asyncio import AsyncSession
from .. import oauth2
from . import generic_exceptions, generic_stmts
from ..models.base_model import Base


async def get_items(
    credentials: HTTPAuthorizationCredentials, session: AsyncSession, model
) -> Sequence:
    credentials_id = oauth2.decode_token(credentials.credentials)
    select_stmt = select(model).where(model.user_id == credentials_id)
    return await generic_stmts.exec_select_stmt(select_stmt, session, all=True)


async def get_item(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    session: AsyncSession,
    model,
    model_name: str,
) -> any:
    user_id = oauth2.decode_token(credentials.credentials)
    select_stmt = select(model).where(model.id == id)
    item = await generic_stmts.exec_select_stmt(select_stmt, session)

    if item is None:
        raise generic_exceptions.NOT_FOUND_EXCEPTION(model_name, id)
    if item.user_id != user_id:
        raise generic_exceptions.FORBIDDEN_EXCEPTION
    return item


async def create_item(
    credentials: HTTPAuthorizationCredentials,
    session: AsyncSession,
    model,
    data=None,
    additional_data: dict = {},
) -> any:
    user_id = oauth2.decode_token(credentials.credentials)
    created_item = (
        model(**data.model_dump(), **additional_data, user_id=user_id)
        if data is not None
        else model(**additional_data, user_id=user_id)
    )
    await generic_stmts.add_to_db(created_item, session)
    return created_item


async def delete_item(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    session: AsyncSession,
    model,
    model_name: str,
) -> Response:
    user_id = oauth2.decode_token(credentials.credentials)
    select_stmt = select(model).where(model.id == id)
    item_to_delete = await generic_stmts.exec_select_stmt(select_stmt, session)

    if item_to_delete is None:
        raise generic_exceptions.NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_delete.user_id != user_id:
        raise generic_exceptions.FORBIDDEN_EXCEPTION

    await session.delete(item_to_delete)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def update_item(
    id: int,
    updated_item: BaseModel,
    credentials: HTTPAuthorizationCredentials,
    session: AsyncSession,
    model,
    model_name: str,
) -> any:
    user_id = oauth2.decode_token(credentials.credentials)
    select_stmt = select(model).where(model.id == id)
    item_to_update = await generic_stmts.exec_select_stmt(select_stmt, session)

    if item_to_update is None:
        raise generic_exceptions.NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_update.user_id != user_id:
        raise generic_exceptions.FORBIDDEN_EXCEPTION

    update_stmt = update(model).values(updated_item.model_dump()).returning(model)
    return await generic_stmts.exec_update_stmt(update_stmt, session)


def check_authorization(
    target: Base, parent_class: Base, parent_id: int, connection: Connection
) -> None:
    select_stmt = select(parent_class).where(parent_class.id == parent_id)
    parent = connection.execute(select_stmt).first()
    if parent.user_id != target.user_id:
        raise generic_exceptions.FORBIDDEN_EXCEPTION
