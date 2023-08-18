from datetime import datetime
from pydantic import BaseModel


class BodyWeightInSchema(BaseModel):
    weight: float


class BodyWeightSchema(BodyWeightInSchema):
    id: int
    user_id: int
    date: str
    created_at: datetime
