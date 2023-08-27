from typing import Self
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy import TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from .base_model import Base
from .. import oauth2
from ..utils import generic_stmts


class ProfilePicture(Base):
    __tablename__ = "profile_pictures"

    picture_id: Mapped[str] = mapped_column(TEXT, nullable=False)
    profile_id = mapped_column(
        ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"ProfilePicture(url={self.picture_id}, ...)"

    @classmethod
    async def create_profile_picture(
        cls,
        picture_id: str,
        credentials: HTTPAuthorizationCredentials,
        session: AsyncSession,
    ) -> Self:
        credentials_id = oauth2.decode_token(credentials.credentials)
        created_picture = cls(
            picture_id=picture_id, profile_id=credentials_id, user_id=credentials_id
        )
        await generic_stmts.add_to_db(created_picture, session)
        return created_picture
