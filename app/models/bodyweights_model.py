from sqlalchemy import Float, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class BodyWeight(Base):
    __tablename__ = "body_weights"

    date: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="today"
    )
    weight: Mapped[float] = mapped_column(Float(precision=1), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    def __repr__(self) -> str:
        return f"BodyWeight(date={self.date}, weight={self.weight}, ...)"
