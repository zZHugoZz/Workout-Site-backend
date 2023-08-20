from typing import Sequence
from fastapi import Response, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .. import oauth2
from .generic_exceptions import NOT_FOUND_EXCEPTION, FORBIDDEN_EXCEPTION


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
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
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
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_delete.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    delete_stmt = delete(model).where(model.id == id)
    await session.execute(delete_stmt)
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
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_update.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    update_stmt = update(model).values(updated_item.model_dump()).returning(model)
    exec = await session.execute(update_stmt)
    await session.commit()
    updated_model = exec.scalars().first()
    return updated_model


async def add_to_db(created_item, session: AsyncSession):
    session.add(created_item)
    await session.commit()
    await session.refresh(created_item)
