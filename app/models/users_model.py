from typing import Self
from fastapi import HTTPException, status
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from ..utils import generic_operations, encryption
from .base_model import Base
from ..schemas import users_schemas
from .profiles_model import Profile
from .units_model import Unit


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username} email={self.email})"

    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[Self]:
        query = select(cls)
        users = await session.execute(query)
        return users.scalars()

    @classmethod
    async def get_user(cls, session: AsyncSession, id: int) -> Self:
        select_stmt = select(cls).where(cls.id == id)
        exec = await session.execute(select_stmt)
        user = exec.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} doesn't exist",
            )
        return user

    @classmethod
    async def create_user(
        cls, user: users_schemas.UserInSchema, session: AsyncSession
    ) -> Self:
        user.password = encryption.hash(user.password)
        created_user = cls(**user.model_dump())
        await generic_operations.add_to_db(created_user, session)
        created_profile = Profile(
            username=created_user.username,
            email=created_user.email,
            user_id=created_user.id,
        )
        await generic_operations.add_to_db(created_profile, session)
        created_unit = Unit(user_id=created_user.id)
        await generic_operations.add_to_db(created_unit, session)
        return created_user
