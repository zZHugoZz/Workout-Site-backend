from typing import Annotated
from fastapi import Depends, status, HTTPException, APIRouter, Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from ..utils import verify
from ..oauth2 import encode_token, encode_refresh_token, get_new_access_token


router = APIRouter(tags=["Authentication"])
security = HTTPBearer()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User).filter(models.User.email == credentials.username).first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encode_token(user.id)
    refresh_token = encode_refresh_token(user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh_token")
def refresh(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    return get_new_access_token(token, db)
