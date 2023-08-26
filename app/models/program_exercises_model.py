from sqlalchemy import ForeignKey, String, event, Connection
from sqlalchemy.orm import Mapped, mapped_column, Mapper
from .base_model import Base
from .program_days_model import ProgramDay
from ..utils import generic_operations


class ProgramExercise(Base):
    __tablename__ = "program_exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    min_sets: Mapped[int] = mapped_column(nullable=False)
    max_sets: Mapped[int] = mapped_column(nullable=False)
    min_reps: Mapped[int] = mapped_column(nullable=False)
    max_reps: Mapped[int] = mapped_column(nullable=False)
    day_id: Mapped[int] = mapped_column(
        ForeignKey("program_days.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"ProgramExercise(name={self.name}, min_sets={self.min_sets}, max_sets={self.max_sets}, ...)"


class ProgramExerciseEvents:
    @staticmethod
    @event.listens_for(ProgramExercise, "before_insert")
    def add_program_exercise_auth(
        mapper: Mapper, connection: Connection, target: ProgramExercise
    ) -> None:
        generic_operations.check_authorization(
            target, ProgramDay, target.day_id, connection
        )
