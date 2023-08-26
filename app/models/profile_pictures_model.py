from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base_model import Base


class ProfilePicture(Base):
    __tablename__ = "profile_pictures"

    url: Mapped[str] = mapped_column(TEXT, nullable=False)
    profile_id = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"ProfilePicture(url={self.url}, ...)"
