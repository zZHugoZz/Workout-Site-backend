from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .users import User


class Program(BaseModel):
    __tablename__ = "programs"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="New program"
    )
    description: Mapped[str] = mapped_column(
        String(300), nullable=False, server_default="No description"
    )
    n_days: Mapped[int] = mapped_column(nullable=False, server_default="7")
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()
    days: Mapped[list["ProgramDay"]] = relationship()

    def __repr__(self) -> str:
        return f"Program(name={self.name}, description={self.description}, n_days={self.n_days}, ...)"


class ProgramDay(BaseModel):
    __tablename__ = "program_days"

    program_id = mapped_column(
        ForeignKey("programs.id", ondelete="CASCADE"), nullable=False
    )
    exercises: Mapped[list["ProgramExercise"]] = relationship()
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"ProgramDay(program_id={self.program_id}, exercises={self.exercises}, ...)"
        )


class ProgramExercise(BaseModel):
    __tablename__ = "program_exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    min_sets: Mapped[int] = mapped_column(nullable=False)
    max_sets: Mapped[int] = mapped_column(nullable=False)
    min_reps: Mapped[int] = mapped_column(nullable=False)
    max_reps: Mapped[int] = mapped_column(nullable=False)
    day_id = mapped_column(
        ForeignKey("program_days.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"ProgramExercise(name={self.name}, min_sets={self.min_sets}, max_sets={self.max_sets}, ...)"
