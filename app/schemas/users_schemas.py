from datetime import datetime
from pydantic import BaseModel, EmailStr


class BaseUserSchema(BaseModel):
    username: str
    email: EmailStr


class UserInSchema(BaseUserSchema):
    password: str


class UserOutSchema(BaseUserSchema):
    id: int
    created_at: datetime
