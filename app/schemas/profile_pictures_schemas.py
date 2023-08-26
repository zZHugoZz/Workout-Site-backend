from datetime import datetime
from pydantic import BaseModel


class ProfilePictureSchema(BaseModel):
    id: int
    url: str
    profile_id: int
    user_id: int
    created_at: datetime
