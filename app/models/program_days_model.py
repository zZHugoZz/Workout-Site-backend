from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, event, Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship, Mapper
from .base_model import Base
from ..utils import generic_operations
from .programs_model import Program

if TYPE_CHECKING:
    from .program_exercises_model import ProgramExercise


class ProgramDay(Base):
    __tablename__ = "program_days"

    program_id: Mapped[int] = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE")
    )
    exercises: Mapped[list["ProgramExercise"]] = relationship(
        "ProgramExercise", lazy="selectin", cascade="all, delete"
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"ProgramDay(program_id={self.program_id}, exercises={self.exercises}, ...)"
        )


class ProgramDayEvents:
    @staticmethod
    @event.listens_for(ProgramDay, "before_insert")
    def add_program_day_auth(
        mapper: Mapper, connection: Connection, target: ProgramDay
    ) -> None:
        generic_operations.check_authorization(
            target, Program, target.program_id, connection
        )
