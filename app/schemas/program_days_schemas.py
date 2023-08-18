from pydantic import BaseModel
from .program_exercises_schemas import ProgramExerciseSchema


class ProgramDayInSchema(BaseModel):
    program_id: int


class ProgramDaySchema(ProgramDayInSchema):
    id: int
    exercises: list[ProgramExerciseSchema]
