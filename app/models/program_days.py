from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .program_exercises import ProgramExercise


class ProgramDay(Base):
    __tablename__ = "program_days"

    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE")
    )
    exercises: Mapped[list["ProgramExercise"]] = relationship("ProgramExercise")
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"ProgramDay(program_id={self.program_id}, exercises={self.exercises}, ...)"
        )
