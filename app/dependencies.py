from typing import Annotated
from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db


security = HTTPBearer()


def get_credendials_and_db(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
):
    return {"credentials": credentials, "db": db}


common_deps = Annotated[dict, Depends(get_credendials_and_db)]
