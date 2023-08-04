from fastapi import HTTPException, Response, status
from fastapi.security import HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.oauth2 import decode_token
from . import schemas


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.hash(password)


def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to perform this action",
)


def NOT_FOUND_EXCEPTION(name: str, id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{name.capitalize()} with id: {id} doesn't exist",
    )


def get_items(credentials: HTTPAuthorizationCredentials, db: Session, model):
    user_id = decode_token(credentials.credentials)
    items = db.query(model).filter(model.user_id == user_id).all()
    return items


def get_item(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    db: Session,
    model,
    model_name: str,
):
    user_id = decode_token(credentials.credentials)
    query = db.query(model).filter(model.id == id)
    if query.first() is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    return query.first()


def create(
    credentials: HTTPAuthorizationCredentials,
    db: Session,
    model,
    data=None,
    additional_data: dict = {},
):
    user_id = decode_token(credentials.credentials)
    created_item = (
        model(**data.model_dump(), **additional_data, user_id=user_id)
        if data is not None
        else model(**additional_data, user_id=user_id)
    )
    db.add(created_item)
    db.commit()
    db.refresh(created_item)
    return created_item


def delete(
    id: int,
    credentials: HTTPAuthorizationCredentials,
    db: Session,
    model,
    model_name: str,
):
    user_id = decode_token(credentials.credentials)
    query = db.query(model).filter(model.id == id)
    if query.first() is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(
    id: int,
    updated_item,
    credentials: HTTPAuthorizationCredentials,
    db: Session,
    model,
    model_name: str,
):
    user_id = decode_token(credentials.credentials)
    query = db.query(model).filter(model.id == id)
    if query.first() is None:
        raise NOT_FOUND_EXCEPTION(model_name, id)
    if query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    query.update(updated_item.model_dump())
    db.commit()
    return query.first()


def add_to_db(created_item, db: Session):
    db.add(created_item)
    db.commit()
    db.refresh(created_item)
