from typing import Mapping
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .config import settings
from .models import blacklisted_tokens as blt


SECRET_KEY = settings.secret_key
REFRESH_SECRET_KEY = settings.refresh_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes


def encode_token(user_id: int) -> bytes:
    payload = {
        "exp": datetime.utcnow()
        + timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "scope": "access_token",
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] != "access_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Scope for the token is invalid",
            )
        return payload["sub"]

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def encode_refresh_token(user_id: int) -> bytes:
    payload = {
        "exp": datetime.utcnow()
        + timedelta(days=0, minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "scope": "refresh_token",
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_new_access_token(
    refresh_token: str, session: AsyncSession
) -> dict[str, bytes]:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] != "refresh_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid scope for token",
            )
        select_stmt = select(blt.BlackListedToken).where(
            blt.BlackListedToken.token == refresh_token
        )
        exec = await session.execute(select_stmt)
        blacklisted_token = exec.scalars().first()
        if blacklisted_token is not None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
            )
        user_id = payload["sub"]
        new_token = encode_token(user_id)
        new_refresh_token = encode_refresh_token(user_id)
        used_token = blt.BlackListedToken(token=refresh_token)
        session.add(used_token)
        await session.commit()
        return {"access_token": new_token, "refresh_token": new_refresh_token}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
