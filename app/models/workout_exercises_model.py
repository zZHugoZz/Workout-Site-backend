from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, event, Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from .base_model import Base
from .workouts_model import Workout
from ..utils import generic_operations

if TYPE_CHECKING:
    from .workout_exercise_sets_model import WorkoutExerciseSet


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    n_sets: Mapped[int] = mapped_column(nullable=False, server_default="0")
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE")
    )
    sets: Mapped[list["WorkoutExerciseSet"]] = relationship(
        "WorkoutExerciseSet", lazy="selectin", cascade="all, delete"
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"WorkoutExercise(id={self.id}, name={self.name}, nsets={self.n_sets}, ...)"
        )


class WorkoutExerciseEvents:
    @staticmethod
    @event.listens_for(WorkoutExercise, "before_insert")
    def add_workout_exercise_auth(
        mapper: Mapper, connection: Connection, target: WorkoutExercise
    ) -> None:
        generic_operations.check_authorization(
            target, Workout, target.workout_id, connection
        )
