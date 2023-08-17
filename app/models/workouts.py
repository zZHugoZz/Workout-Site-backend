from sqlalchemy import Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .users import User


class Workout(BaseModel):
    __tablename__ = "workouts"

    date: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="today"
    )
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship()
    exercises: Mapped[list["WorkoutExercise"]] = relationship()

    def __repr__(self) -> str:
        return f"Workout(id={self.id}, date={self.date}, ...)"


class WorkoutExercise(BaseModel):
    __tablename__ = "workout_exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    n_sets: Mapped[int] = mapped_column(nullable=False, server_default="0")
    workout_id = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False
    )
    sets: Mapped[list["WorkoutExerciseSet"]] = relationship("WorkoutExerciseSet")

    def __repr__(self) -> str:
        return (
            f"WorkoutExercise(id={self.id}, name={self.name}, nsets={self.n_sets}, ...)"
        )


class WorkoutExerciseSet(BaseModel):
    __tablename__ = "workout_exercise_sets"

    reps: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    workout_exercise_id: Mapped[int] = mapped_column(
        ForeignKey("workout_exercises.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"WorkoutExerciseSet(id={self.id}, reps={self.reps}, weight={self.weight}, ...)"
