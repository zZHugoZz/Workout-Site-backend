from typing import Annotated
from enum import auto
from strenum import LowercaseStrEnum
from fastapi import Security, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db


security = HTTPBearer()


class Dependencies(LowercaseStrEnum):
    CREDENTIALS = auto()
    DB = auto()


def get_credendials_and_db(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: AsyncSession = Depends(get_db),
):
    return {Dependencies.CREDENTIALS: credentials, Dependencies.DB: db}


common_deps = Annotated[dict, Depends(get_credendials_and_db)]
