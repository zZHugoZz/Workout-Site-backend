from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class BlackListedToken(BaseModel):
    __tablename__ = "blacklisted_tokens"

    token: Mapped[str] = mapped_column(String(300), nullable=False)

    def __repr__(self) -> str:
        f"BlackListedToken(id={self.id}, token={self.token})"
