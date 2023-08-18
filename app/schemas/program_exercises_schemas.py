from pydantic import BaseModel


class ProgramExerciseInSchema(BaseModel):
    name: str
    min_sets: int
    max_sets: int
    min_reps: int
    max_reps: int
    day_id: int


class ProgramExerciseSchema(ProgramExerciseInSchema):
    id: int
