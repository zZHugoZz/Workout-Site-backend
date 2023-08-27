from typing import Self
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import Float, ForeignKey, String, select, update
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from app import oauth2
from app.schemas import bodyweights_schemas
from .base_model import Base
from ..utils import generic_stmts


class BodyWeight(Base):
    __tablename__ = "body_weights"

    date: Mapped[str] = mapped_column(String(100), nullable=False)
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"BodyWeight(date={self.date}, weight={self.weight}, ...)"

    @classmethod
    async def add_bodyweight(
        cls,
        current_date,
        bodyweight_in: bodyweights_schemas.BodyWeightInSchema,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
    ) -> Self:
        credentials_id = oauth2.decode_token(credentials.credentials)
        select_dy_date_stmt = select(cls).where(cls.date == current_date)
        bodyweight: BodyWeight = await generic_stmts.exec_select_stmt(
            select_dy_date_stmt, session
        )
        print("bodyweight: ", bodyweight)

        if bodyweight is not None:
            update_stmt = (
                update(cls)
                .where(cls.id == bodyweight.id)
                .values({"weight": bodyweight_in.weight})
                .returning(cls)
            )
            return await generic_stmts.exec_update_stmt(update_stmt, session)

        created_bodyweight = cls(
            **bodyweight_in.model_dump(), date=current_date, user_id=credentials_id
        )
        await generic_stmts.add_to_db(created_bodyweight, session)
        return created_bodyweight
