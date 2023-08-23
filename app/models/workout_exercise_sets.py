from sqlalchemy import ForeignKey, Float, Connection, event, update
from sqlalchemy.orm import Mapped, mapped_column, Mapper
from .base import Base
from .workout_exercises import WorkoutExercise
from ..utils import generic_operations


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


class WorkoutExerciseSetEvents:
    @staticmethod
    @event.listens_for(WorkoutExerciseSet, "after_insert")
    def increment_n_sets(
        mapper: Mapper, connection: Connection, target: WorkoutExerciseSet
    ) -> None:
        """increments n_sets of the workout_exercises table when a set is created"""
        update_stmt = (
            update(WorkoutExercise)
            .where(WorkoutExercise.id == target.workout_exercise_id)
            .values({"n_sets": WorkoutExercise.n_sets + 1})
        )
        connection.execute(update_stmt)

    @staticmethod
    @event.listens_for(WorkoutExerciseSet, "after_delete")
    def decrement_n_sets(
        mapper: Mapper, connection: Connection, target: WorkoutExerciseSet
    ) -> None:
        """decrements n_sets of the workout_exercises table when a set is created"""
        update_stmt = (
            update(WorkoutExercise)
            .where(WorkoutExercise.id == target.workout_exercise_id)
            .values({"n_sets": WorkoutExercise.n_sets - 1})
        )
        connection.execute(update_stmt)

    @staticmethod
    @event.listens_for(WorkoutExerciseSet, "before_insert")
    def add_workout_exercise_set_auth(
        mapper: Mapper, connection: Connection, target: WorkoutExerciseSet
    ) -> None:
        generic_operations.check_authorization(
            target, WorkoutExercise, target.workout_exercise_id, connection
        )
