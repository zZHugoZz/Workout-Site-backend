from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import models
from ..database import get_db
from .. import schemas


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await models.User.get_users(db)
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await models.User.get_user(db, id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} doesn't exist",
        )
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):
    created_user = await models.User.create_user(user, db)
    return created_user
