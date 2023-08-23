from typing import Sequence
from fastapi import Response, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import select, update, Connection
from sqlalchemy.ext.asyncio import AsyncSession
from .. import oauth2
from . import generic_exceptions
from ..models.base import Base


async def get_items(
    credentials: HTTPAuthorizationCredentials, session: AsyncSession, model
) -> Sequence:
    user_id = oauth2.decode_token(credentials.credentials)
    query = select(model).where(model.user_id == user_id)
    exec = await session.execute(query)
    items = exec.scalars().all()
    return items


async def get_item(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    session: AsyncSession,
    model,
    model_name: str,
) -> any:
    user_id = oauth2.decode_token(credentials.credentials)
    query = select(model).where(model.id == id)
    exec = await session.execute(query)
    item = exec.scalars().first()

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
    await add_to_db(created_item, session)
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
    exec = await session.execute(select_stmt)
    item_to_delete = exec.scalars().first()

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
    exec = await session.execute(select_stmt)
    item_to_update = exec.scalars().first()

    if item_to_update is None:
        raise generic_exceptions.NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_update.user_id != user_id:
        raise generic_exceptions.FORBIDDEN_EXCEPTION

    update_stmt = update(model).values(updated_item.model_dump()).returning(model)
    exec = await session.execute(update_stmt)
    await session.commit()
    updated_model = exec.scalars().first()
    return updated_model


async def add_to_db(created_item, session: AsyncSession):
    session.add(created_item)
    await session.commit()
    await session.refresh(created_item)


def check_authorization(
    target: Base, parent_class: Base, parent_id: int, connection: Connection
) -> None:
    """
    checks if the user that created the instance corresponds to the one who
    created the corresponding parent instance
    """
    select_stmt = select(parent_class).where(parent_class.id == parent_id)
    parent = connection.execute(select_stmt).first()
    if parent.user_id != target.user_id:
        raise generic_exceptions.FORBIDDEN_EXCEPTION
