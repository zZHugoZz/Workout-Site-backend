from typing import Annotated
from fastapi import Depends, status, HTTPException, APIRouter, Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users
from ..database import get_db
from .. import schemas
from ..utils import encryption
from .. import oauth2


router = APIRouter(tags=["Authentication"])
security = HTTPBearer()


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
):
    select_stmt = select(users.User).where(users.User.email == credentials.username)
    exec = await db.execute(select_stmt)
    user = exec.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    if not encryption.verify(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth2.encode_token(user.id)
    refresh_token = oauth2.encode_refresh_token(user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.get("/refresh_token")
def refresh(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    print(token)
    return oauth2.get_new_access_token(token, db)
