from typing import Self, Sequence
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from .base_model import Base


class Exercise(Base):
    __tablename__ = "exercises"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    link: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"Exercise(name={self.name}, link={self.link}, ...)"

    @classmethod
    async def get_exercises(cls, session: AsyncSession) -> Sequence[Self | None]:
        select_stmt = select(cls)
        exec = await session.execute(select_stmt)
        exercises = exec.scalars().all()
        return exercises
