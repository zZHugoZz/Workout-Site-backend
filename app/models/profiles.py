from typing import Self, TYPE_CHECKING
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr
from sqlalchemy import String, ForeignKey, select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from .. import oauth2

if TYPE_CHECKING:
    from .users import User


class Profile(Base):
    __tablename__ = "profiles"

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(100), nullable=True)
    profile_picture: Mapped[bytes] = mapped_column(BYTEA, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        "User", back_populates="profile", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, username={self.username}, email={self.email}, user_id={self.user_id}, user={self.user})"

    @classmethod
    async def get_profile(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> Self:
        credentials_id = oauth2.decode_token(credentials.credentials)
        select_stmt = select(cls).filter(cls.user_id == credentials_id)
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
