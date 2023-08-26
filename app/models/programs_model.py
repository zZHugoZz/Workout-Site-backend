from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base
from .users_model import User

if TYPE_CHECKING:
    from .program_days_model import ProgramDay


class Program(Base):
    __tablename__ = "programs"

    name: Mapped[str] = mapped_column(
        String(100), nullable=False, server_default="New program"
    )
    description: Mapped[str] = mapped_column(
        String(300), nullable=False, server_default="No description"
    )
    n_days: Mapped[int] = mapped_column(nullable=False, server_default="7")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship("User", lazy="selectin")
    days: Mapped[list["ProgramDay"]] = relationship(
        "ProgramDay", lazy="selectin", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"Program(name={self.name}, description={self.description}, n_days={self.n_days}, ...)"
