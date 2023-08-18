from pydantic import BaseModel
from .users_schemas import UserOutSchema


class ProfileInSchema(BaseModel):
    age: int
    gender: str
    profile_picture: bytes | None = None


class ProfileSchema(ProfileInSchema):
    user_id: int
    user: UserOutSchema
