from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users
from ..database import get_db
from ..schemas import users_schemas


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[users_schemas.UserOutSchema],
)
async def get_users(db: AsyncSession = Depends(get_db)):
    retrieved_users = await users.User.get_users(db)
    return retrieved_users


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=users_schemas.UserOutSchema
)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await users.User.get_user(db, id)
    return user


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=users_schemas.UserOutSchema
)
async def create_user(
    user: users_schemas.UserInSchema, db: AsyncSession = Depends(get_db)
):
    created_user = await users.User.create_user(user, db)
    return created_user
