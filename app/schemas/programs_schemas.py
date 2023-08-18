from datetime import datetime
from pydantic import BaseModel
from .program_days_schemas import ProgramDaySchema


class ProgramInSchema(BaseModel):
    name: str
    description: str
    n_days: int


class ProgramSchema(ProgramInSchema):
    id: int
    user_id: int
    days: list[ProgramDaySchema]
    created_at: datetime
