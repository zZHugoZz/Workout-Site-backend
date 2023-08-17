from typing import Annotated
from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from .routers.authentication import security, get_db


def get_credendials_and_db(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
):
    return {"credentials": credentials, "db": db}


common_deps = Annotated[dict, Depends(get_credendials_and_db)]
