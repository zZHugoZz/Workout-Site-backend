from sqlalchemy import Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import BaseModel
from .users import User


class BodyWeight(BaseModel):
    __tablename__ = "body_weights"

    date: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="today"
    )
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship()

    def __repr__(self) -> str:
        return f"BodyWeight(date={self.date}, weight={self.weight}, ...)"