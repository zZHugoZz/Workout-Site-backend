from datetime import datetime
from pydantic import BaseModel, ConfigDict
from .performances_schemas import PerformanceSchema


class ProgresionInSchema(BaseModel):
    name: str
    color: str


class ProgressionSchema(ProgresionInSchema):
    id: int
    created_at: datetime
    user_id: int
    performances: list[PerformanceSchema]

    model_config = ConfigDict(from_attributes=True)
