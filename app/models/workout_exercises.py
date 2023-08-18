from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .workout_exercise_sets import WorkoutExerciseSet


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    n_sets: Mapped[int] = mapped_column(nullable=False, server_default="0")
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE")
    )
    sets: Mapped[list[WorkoutExerciseSet]] = relationship("WorkoutExerciseSet")

    def __repr__(self) -> str:
        return (
            f"WorkoutExercise(id={self.id}, name={self.name}, nsets={self.n_sets}, ...)"
        )
