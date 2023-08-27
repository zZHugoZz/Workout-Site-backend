from typing import Self
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import Float, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import bodyweights_schemas
from .base_model import Base


class BodyWeight(Base):
    __tablename__ = "body_weights"

    date = mapped_column(Date, nullable=False, server_default="today")
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"BodyWeight(date={self.date}, weight={self.weight}, ...)"

    @classmethod
    async def add_bodyweight(
        cls,
        bodyweight_in: bodyweights_schemas.BodyWeightInSchema,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
    ) -> Self:
        pass
