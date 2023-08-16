from fastapi import Depends, status, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.users import User
from ..database import get_db
from .. import schemas


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await User.get_users(db)
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await User.get_user(db, id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):
    print("user:", user)
    created_user = await User.create_user(user, db)
    print("created_users: ", created_user)
    return created_user
