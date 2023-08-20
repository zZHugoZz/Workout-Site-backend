from typing import Self
import datetime
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from .. import oauth2
from .base import Base
from .users import User
from .workout_exercises import WorkoutExercise
from ..utils import generic_operations


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
    async def create_workout(
        cls, credentials: HTTPAuthorizationCredentials, session: AsyncSession
    ) -> Self:
        credentials_id = oauth2.decode_token(credentials.credentials)
        current_date = datetime.date.today()
        day, month, year = current_date.day, current_date.month, current_date.year
        created_workout = cls(
            date=str(current_date),
            day=day,
            month=month,
            year=year,
            user_id=credentials_id,
        )
        await generic_operations.add_to_db(created_workout, session)
        return created_workout
