from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
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

    @classmethod
    async def get_n_sets(cls, id: int, session: AsyncSession) -> int:
        s = select(cls).where(cls.id == id)
        exec = await session.execute(s)
        i = exec.scalars().first()
        return len(i.sets)
