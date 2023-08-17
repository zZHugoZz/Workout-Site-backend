from typing import Sequence
from fastapi import HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy import select, update, insert
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.oauth2 import decode_token


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------- encryption --------------------
def hash(password: str) -> str:
    return pwd_context.hash(password)


def verify(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# -------------------- custom exceptions --------------------
FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to perform this action",
)


def NOT_FOUND_EXCEPTION(name: str, id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{name.capitalize()} with id: {id} doesn't exist",
    )


# -------------------- CRUD operations --------------------
async def get_items(
    credentials: HTTPAuthorizationCredentials, db: AsyncSession, model
) -> Sequence:
    # user_id = decode_token(credentials.credentials)
    # items = db.query(model).filter(model.user_id == user_id).all()
    # return items
    user_id = decode_token(credentials.credentials)
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
    # user_id = decode_token(credentials.credentials)
    # query = db.query(model).filter(model.id == id)
    # if query.first() is None:
    #     raise NOT_FOUND_EXCEPTION(model_name, id)
    # if query.first().user_id != user_id:
    #     raise FORBIDDEN_EXCEPTION
    # return query.first()
    user_id = decode_token(credentials.credentials)
    query = select(model).where(model.id == id)
    exec = await db.execute(query)
    item = exec.scalars().first()
    if item is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    return item


async def create(
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
    model,
    data=None,
    additional_data: dict = {},
) -> any:
    user_id = decode_token(credentials.credentials)
    created_item = (
        model(**data.model_dump(), **additional_data, user_id=user_id)
        if data is not None
        else model(**additional_data, user_id=user_id)
    )
    # db.add(created_item)
    # db.commit()
    # db.refresh(created_item)
    # return created_item
    await add_to_db(created_item, db)
    return created_item


async def delete(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
    model,
    model_name: str,
) -> Response:
    user_id = decode_token(credentials.credentials)
    # query = db.query(model).filter(model.id == id)
    # if query.first() is None:
    #     raise NOT_FOUND_EXCEPTION(model_name, id)
    # if query.first().user_id != user_id:
    #     raise FORBIDDEN_EXCEPTION
    # query.delete()
    # db.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    query = select(model).where(model.id == id)
    exec = await db.execute(query)
    item_to_delete = exec.scalars().first()
    if item_to_delete is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if item_to_delete.user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    db.delete(item_to_delete)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def update(
    id: int,
    updated_item,
    credentials: HTTPAuthorizationCredentials,
    db: AsyncSession,
    model,
    model_name: str,
) -> any:
    user_id = decode_token(credentials.credentials)
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
    return model


async def add_to_db(created_item, db: AsyncSession):
    db.add(created_item)
    await db.commit()
    await db.refresh(created_item)
