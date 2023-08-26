from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import users_model
from ..database import get_db
from ..schemas import users_schemas


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[users_schemas.UserOutSchema],
)
async def get_users(db: AsyncSession = Depends(get_db)):
    return await users_model.User.get_users(db)


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=users_schemas.UserOutSchema
)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    return await users_model.User.get_user(db, id)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=users_schemas.UserOutSchema
)
async def create_user(
    user: users_schemas.UserInSchema, db: AsyncSession = Depends(get_db)
):
    return await users_model.User.create_user(user, db)
