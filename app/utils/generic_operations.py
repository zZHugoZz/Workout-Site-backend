from typing import Sequence
from fastapi import Response, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from .. import oauth2
from .generic_exceptions import NOT_FOUND_EXCEPTION, FORBIDDEN_EXCEPTION


async def get_items(
    credentials: HTTPAuthorizationCredentials, db: AsyncSession, model
) -> Sequence:
    user_id = oauth2.decode_token(credentials.credentials)
    query = select(model).where(model.user_id == user_id)
    exec = await db.execute(query)
    items = exec.scalars().all()
    return items


async def get_item(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
    model,
    model_name: str,
) -> any:
    user_id = oauth2.decode_token(credentials.credentials)
    query = select(model).where(model.id == id)
    exec = await db.execute(query)
    item = exec.scalars().first()
    if item is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    return item


async def create_item(
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
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
    await add_to_db(created_item, db)
    return created_item


async def delete_item(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
    model,
    model_name: str,
) -> Response:
    user_id = oauth2.decode_token(credentials.credentials)
    query = select(model).where(model.id == id)
    exec = await db.execute(query)
    item_to_delete = exec.scalars().first()
    if item_to_delete is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_delete.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    await db.delete(item_to_delete)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


""" Take a look later """


async def update_item(
    id: int,
    updated_item,
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
    model,
    model_name: str,
) -> any:
    user_id = oauth2.decode_token(credentials.credentials)
    # query = db.query(model).filter(model.id == id)
    # if query.first() is None:
    #     raise NOT_FOUND_EXCEPTION(model_name, id)
    # if query.first().user_id != user_id:
    #     raise FORBIDDEN_EXCEPTION
    # query.update(updated_item.model_dump())
    # db.commit()
    # return query.first()
    query = select(model).where(model.id == id)
    exec = await db.execute(query)
    item_to_update = exec.scalars().first()
    if item_to_update is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_update.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    query = update(model).values(updated_item.model_dump())
    await db.execute(query)
    await db.commit()
    return model


async def add_to_db(created_item, db: AsyncSession):
    db.add(created_item)
    await db.commit()
    await db.refresh(created_item)
