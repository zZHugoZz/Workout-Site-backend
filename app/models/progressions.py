from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .users import User

if TYPE_CHECKING:
    from .performances import Performance


class Progression(Base):
    __tablename__ = "progressions"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="#40FA84"
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User")
    performances: Mapped[list["Performance"]] = relationship(
        "Performance", back_populates="progression", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"Progression(name={self.name}, color={self.color}, ...)"
