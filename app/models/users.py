from typing import Self
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr
from sqlalchemy import String, select, ForeignKey, update
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import BYTEA
from ..utils import generic_operations
from .base import BaseModel
from .. import schemas
from .. import oauth2


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    profile: Mapped["Profile"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username} email={self.email})"

    @classmethod
    async def get_users(cls, session: AsyncSession) -> list[Self]:
        query = select(cls)
        users = await session.execute(query)
        return users.scalars()

    @classmethod
    async def get_user(cls, session: AsyncSession, id: int) -> Self:
        query = select(cls).where(cls.id == id)
        exec = await session.execute(query)
        user = exec.scalars().first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} doesn't exist",
            )
        return user

    @classmethod
    async def create_user(cls, user: schemas.UserIn, session: AsyncSession) -> Self:
        user.password = hash(user.password)
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


class Profile(BaseModel):
    __tablename__ = "profiles"

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(100), nullable=True)
    profile_picture: Mapped[bytes] = mapped_column(BYTEA, nullable=True)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="profile")

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, username={self.username}, email={self.email}, user_id={self.user_id})"

    @classmethod
    async def get_profile(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> Self:
        user_id = oauth2.decode_token(credentials.credentials)
        select_stmt = select(cls).where(cls.user_id == user_id)
        exec = await session.execute(select_stmt)
        profile = exec.scalars().first()
        return profile

    @classmethod
    async def update_profile(
        cls,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
        new_values: dict,
    ) -> Self:
        user_id = oauth2.decode_token(credentials.credentials)
        update_stmt = update(cls).where(cls.user_id == user_id).values(new_values)
        exec = await session.execute(update_stmt)
        updated_profile = exec.fetchone()
        return updated_profile


class Unit(BaseModel):
    __tablename__ = "units"

    unit: Mapped[str] = mapped_column(String(100), nullable=False, server_default="Kg")
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self) -> str:
        return f"Unit(id={self.id}, unit={self.unit}, user_id={self.user_id})"

    @classmethod
    async def get_unit(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> Self:
        user_id = oauth2.decode_token(credentials.credentials)
        select_stmt = select(cls).where(cls.user_id == user_id)
        exec = await session.execute(select_stmt)
        unit = exec.scalars().first()
        return unit

    @classmethod
    async def update_unit(
        cls,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
        new_values: dict,
    ) -> Self:
        user_id = oauth2.decode_token(credentials.credentials)
        update_stmt = update(cls).where(cls.user_id == user_id).values(new_values)
        exec = await session.execute(update_stmt)
        updated_unit = exec.fetchone()
        return updated_unit
