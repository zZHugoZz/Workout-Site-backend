from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta
from .config import settings
from . import models


SECRET_KEY = settings.secret_key
REFRESH_SECRET_KEY = settings.refresh_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes


def encode_token(user_id):
    payload = {
        "exp": datetime.utcnow()
        + timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "scope": "access_token",
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] == "access_token":
            return payload["sub"]

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Scope for the token is invalid",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


def encode_refresh_token(user_id):
    payload = {
        "exp": datetime.utcnow()
        + timedelta(days=0, minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.utcnow(),
        "scope": "refresh_token",
        "sub": user_id,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_new_access_token(refresh_token, db):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["scope"] == "refresh_token":
            if (
                db.query(models.BlackListedToken)
                .filter(models.BlackListedToken.token == refresh_token)
                .first()
                is not None
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token"
                )

            user_id = payload["sub"]
            new_token = encode_token(user_id)
            new_refresh_token = encode_refresh_token(user_id)
            used_token = models.BlackListedToken(token=refresh_token)
            db.add(used_token)
            db.commit()
            return {"access_token": new_token, "refresh_token": new_refresh_token}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token"
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
