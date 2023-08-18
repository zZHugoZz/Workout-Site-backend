from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Performance(Base):
    __tablename__ = "performances"

    date: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="today"
    )
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    progression_id: Mapped[int] = mapped_column(
        ForeignKey("progressions.id", ondelete="CASCADE")
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Performance(date={self.date}, weight={self.weight}, ...)"
