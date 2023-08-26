from pydantic import BaseModel, EmailStr
from .users_schemas import UserOutSchema
from .profile_pictures_schemas import ProfilePictureSchema


class ProfileInSchema(BaseModel):
    age: int | None = None
    gender: str | None = None


class ProfileSchema(ProfileInSchema):
    username: str
    email: EmailStr
    bodyweight: float | None
    user_id: int
    user: UserOutSchema
    profile_picture: ProfilePictureSchema | None
