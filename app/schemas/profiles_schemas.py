from pydantic import BaseModel, ConfigDict, EmailStr
from .users_schemas import UserOutSchema


class ProfileInSchema(BaseModel):
    age: int | None = None
    gender: str | None = None
    profile_picture: bytes | None = None


class ProfileSchema(ProfileInSchema):
    username: str
    email: EmailStr
    user_id: int
    user: UserOutSchema
