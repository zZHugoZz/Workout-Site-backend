from pydantic import BaseModel, EmailStr
from .users_schemas import UserOutSchema


class ProfileInSchema(BaseModel):
    age: int | None
    gender: str | None
    profile_picture: bytes | None


class ProfileSchema(ProfileInSchema):
    username: str
    email: EmailStr
    bodyweight: float | None
    user_id: int
    user: UserOutSchema
