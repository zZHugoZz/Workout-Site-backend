from datetime import datetime
from pydantic import BaseModel


class PerformanceInSchema(BaseModel):
    date: str
    weight: float
    progression_id: int


class PerformanceSchema(PerformanceInSchema):
    id: int
    created_at: datetime
    user_id: int
