from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


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
