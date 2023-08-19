from pydantic import BaseModel, ConfigDict, EmailStr
from .users_schemas import UserOutSchema


class ProfileInSchema(BaseModel):
    age: int
    gender: str
    profile_picture: bytes | None = None


class ProfileSchema(ProfileInSchema):
    username: str
    email: EmailStr
    user_id: int

    model_config = ConfigDict(from_attributes=True)
