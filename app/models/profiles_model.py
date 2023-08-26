from typing import Self, TYPE_CHECKING
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import EmailStr
from sqlalchemy import Float, String, ForeignKey, select, update, event, Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.asyncio import AsyncSession
from .base_model import Base
from .. import oauth2
from .bodyweights_model import BodyWeight

if TYPE_CHECKING:
    from .users_model import User


class Profile(Base):
    __tablename__ = "profiles"

    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(100), nullable=True)
    profile_picture: Mapped[bytes] = mapped_column(BYTEA, nullable=True)
    bodyweight: Mapped[float] = mapped_column(Float(precision=1), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User", lazy="selectin")

    def __repr__(self) -> str:
        return f"Profile(id={self.id}, username={self.username}, email={self.email}, user_id={self.user_id}, user={self.user})"

    @classmethod
    async def get_profile(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> "Profile":
        credentials_id = oauth2.decode_token(credentials.credentials)
        select_stmt = select(cls).where(cls.user_id == credentials_id)
        exec = await session.execute(select_stmt)
        profile = exec.scalars().first()
        print("user: ", profile.user)
        return profile

    @classmethod
    async def update_profile(
        cls,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
        new_values: dict,
    ) -> Self:
        user_id = oauth2.decode_token(credentials.credentials)
        update_stmt = (
            update(cls).where(cls.user_id == user_id).values(new_values).returning(cls)
        )
        exec = await session.execute(update_stmt)
        await session.commit()
        updated_profile = exec.scalars().first()
        return updated_profile


class ProfileEvents:
    @staticmethod
    @event.listens_for(BodyWeight, "after_insert")
    def update_bodyweight(
        mapper: Mapper, connection: Connection, target: BodyWeight
    ) -> None:
        update_stmt = (
            update(Profile)
            .where(Profile.user_id == target.user_id)
            .values({"bodyweight": target.weight})
            .returning(Profile)
        )
        connection.execute(update_stmt)
        connection.commit()
