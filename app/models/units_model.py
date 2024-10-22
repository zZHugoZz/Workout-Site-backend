from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import String, ForeignKey, select, update
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from .base_model import Base
from .. import oauth2


class Unit(Base):
    __tablename__ = "units"

    unit: Mapped[str] = mapped_column(String(100), nullable=False, server_default="Kg")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"Unit(id={self.id}, unit={self.unit}, user_id={self.user_id})"

    @classmethod
    async def get_unit(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> "Unit":
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
    ) -> "Unit":
        user_id = oauth2.decode_token(credentials.credentials)
        update_stmt = (
            update(cls).where(cls.user_id == user_id).values(new_values).returning(cls)
        )
        exec = await session.execute(update_stmt)
        await session.commit()
        updated_unit = exec.scalars().first()
        return updated_unit
