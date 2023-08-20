from typing import Self, Sequence
import datetime
from fastapi import Response, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.generic_exceptions import FORBIDDEN_EXCEPTION
from .. import oauth2
from .base import Base
from .users import User
from .workout_exercises import WorkoutExercise


class Workout(Base):
    __tablename__ = "workouts"

    date: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="today"
    )
    day: Mapped[int] = mapped_column(nullable=False)
    month: Mapped[int] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User")
    exercises: Mapped[list[WorkoutExercise]] = relationship(
        "WorkoutExercise", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"Workout(id={self.id}, date={self.date}, ...)"

    @classmethod
    async def get_workouts_by_month(
        cls,
        month: int,
        year: int,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
    ) -> Sequence[int] | None:
        credentials_id = oauth2.decode_token(credentials.credentials)
        select_stmt = (
            select(cls.day)
            .where(cls.user_id == credentials_id)
            .where(cls.month == month)
            .where(cls.year == year)
        )
        exec = await session.execute(select_stmt)
        days = exec.scalars().all()
        return days

    @classmethod
    async def get_workout_by_current_date(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> Self | None:
        credentials_id = oauth2.decode_token(credentials.credentials)
        select_stmt = select(cls).where(cls.date == str(datetime.date.today()))
        exec = await session.execute(select_stmt)
        workout = exec.scalars().first()
        if workout is None:
            return Response(status_code=status.HTTP_200_OK)
        if workout.user_id != credentials_id:
            raise FORBIDDEN_EXCEPTION
        return workout
