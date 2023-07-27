from fastapi import HTTPException, status
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password):
    return pwd_context.hash(password)


def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


FORBIDDEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to perform this action",
)
