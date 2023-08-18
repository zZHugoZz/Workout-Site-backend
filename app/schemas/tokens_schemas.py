from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenDataSchema(BaseModel):
    user_id: int


class RefreshTokenSchema(BaseModel):
    refresh_token: str
