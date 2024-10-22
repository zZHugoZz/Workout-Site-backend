from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class BlackListedToken(Base):
    __tablename__ = "blacklisted_tokens"

    token: Mapped[str] = mapped_column(String(300), nullable=False)

    def __repr__(self) -> str:
        return f"BlackListedToken(id={self.id}, token={self.token})"
