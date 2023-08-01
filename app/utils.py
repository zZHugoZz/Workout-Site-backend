from fastapi import HTTPException, status
from passlib.context import CryptContext

from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.oauth2 import decode_token


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


def create(data, credentials: HTTPAuthorizationCredentials, db: Session, model):
    user_id = decode_token(credentials.credentials)
    created_object = model(**data.model_dump(), user_id=user_id)
    db.add(created_object)
    db.commit()
    db.refresh(created_object)
    return created_object
