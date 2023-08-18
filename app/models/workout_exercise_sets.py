from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class WorkoutExerciseSet(Base):
    __tablename__ = "workout_exercise_sets"

    reps: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    workout_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("workout_exercises.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"WorkoutExerciseSet(id={self.id}, reps={self.reps}, weight={self.weight}, ...)"
