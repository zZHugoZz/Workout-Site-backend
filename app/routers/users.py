from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users
from ..database import get_db
from .. import schemas


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await users.User.get_users(db)
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await users.User.get_user(db, id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: AsyncSession = Depends(get_db)):
    created_user = await users.User.create_user(user, db)
    return created_user
