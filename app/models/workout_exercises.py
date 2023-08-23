from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey, event, select, update, Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from .base import Base
from .workouts import Workout
from ..utils import generic_exceptions

if TYPE_CHECKING:
    from .workout_exercise_sets import WorkoutExerciseSet


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
    def check_for_authorization(
        mapper: Mapper, connection: Connection, target: WorkoutExercise
    ) -> None:
        select_stmt = select(Workout).where(Workout.id == target.workout_id)
        workout = connection.execute(select_stmt).first()
        if workout.user_id != target.user_id:
            raise generic_exceptions.FORBIDDEN_EXCEPTION
