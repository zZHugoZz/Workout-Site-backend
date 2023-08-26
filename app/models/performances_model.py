from typing import Self
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import String, ForeignKey, Float, select, update
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from .. import oauth2
from .base_model import Base
from ..schemas import performances_schemas
from ..utils import generic_operations, generic_exceptions
from .progressions_model import Progression
from ..utils import generic_operations


class Performance(Base):
    __tablename__ = "performances"

    date: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="today"
    )
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    progression_id: Mapped[int] = mapped_column(
        ForeignKey("progressions.id", ondelete="CASCADE")
    )
    progression: Mapped["Progression"] = relationship(
        "Progression", back_populates="performances", lazy="selectin"
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Performance(date={self.date}, weight={self.weight}, ...)"

    @classmethod
    async def add_performance(
        cls,
        performance_in: performances_schemas.PerformanceInSchema,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
    ) -> Self:
        credentials_id = oauth2.decode_token(credentials.credentials)
        select_by_date_stmt = select(cls).where(cls.date == performance_in.date)
        exec = await session.execute(select_by_date_stmt)
        performance = exec.scalars().first()

        if performance is not None:
            if performance.progression.user_id != credentials_id:
                raise generic_exceptions.FORBIDDEN_EXCEPTION

            update_stmt = (
                update(cls)
                .where(cls.id == performance.id)
                .values({"weight": performance_in.weight})
                .returning(cls)
            )
            exec = await session.execute(update_stmt)
            await session.commit()
            updated_performance = exec.scalars().first()
            return updated_performance

        created_performance = cls(**performance_in.model_dump(), user_id=credentials_id)
        select_parent_stmt = select(Progression).where(
            Progression.id == created_performance.progression_id
        )
        exec = await session.execute(select_parent_stmt)
        progression = exec.scalars().first()

        if progression.user_id != credentials_id:
            raise generic_exceptions.FORBIDDEN_EXCEPTION

        await generic_operations.add_to_db(created_performance, session)
        return created_performance


class PerformanceEvents:
    pass
