from sqlalchemy import String, ForeignKey, select, event, update, Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from .base import Base
from .workout_exercise_sets import WorkoutExerciseSet


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    n_sets: Mapped[int] = mapped_column(nullable=False, server_default="0")
    workout_id: Mapped[int] = mapped_column(
        ForeignKey("workouts.id", ondelete="CASCADE")
    )
    sets: Mapped[list[WorkoutExerciseSet]] = relationship(
        "WorkoutExerciseSet", lazy="selectin"
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"WorkoutExercise(id={self.id}, name={self.name}, nsets={self.n_sets}, ...)"
        )

    @staticmethod
    @event.listens_for(WorkoutExerciseSet, "after_insert")
    def increment_n_sets(
        mapper: Mapper, connection: Connection, target: WorkoutExerciseSet
    ) -> None:
        update_stmt = (
            update(WorkoutExercise)
            .where(WorkoutExercise.id == target.workout_exercise_id)
            .values({"n_sets": WorkoutExercise.n_sets + 1})
        )
        print("stmt: ", update_stmt)
        connection.execute(update_stmt)

    @staticmethod
    @event.listens_for(WorkoutExerciseSet, "after_delete")
    def decrement_n_sets(
        mapper: Mapper, connection: Connection, target: WorkoutExerciseSet
    ) -> None:
        update_stmt = (
            update(WorkoutExercise)
            .where(WorkoutExercise.id == target.workout_exercise_id)
            .values({"n_sets": WorkoutExercise.n_sets - 1})
        )
        print("stmt: ", update_stmt)
        connection.execute(update_stmt)
        print("mapper: ", type(mapper))
