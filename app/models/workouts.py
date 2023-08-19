from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .users import User
from .workout_exercises import WorkoutExercise


class Workout(Base):
    __tablename__ = "workouts"

    date: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="today"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User")
    exercises: Mapped[list[WorkoutExercise]] = relationship("WorkoutExercise")

    def __repr__(self) -> str:
        return f"Workout(id={self.id}, date={self.date}, ...)"
