from sqlalchemy import Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .users import User


class Progression(BaseModel):
    __tablename__ = "progressions"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="#40FA84"
    )
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship()
    performances: Mapped[list["Performance"]] = relationship()

    def __repr__(self) -> str:
        return f"Progression(name={self.name}, color={self.color}, ...)"


class Performance(BaseModel):
    __tablename__ = "performances"

    date: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="today"
    )
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    progression_id = mapped_column(
        ForeignKey("progressions.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Performance(date={self.date}, weight={self.weight}, ...)"
