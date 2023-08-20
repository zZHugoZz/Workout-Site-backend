from datetime import datetime
from pydantic import BaseModel
from .workout_exercises_schemas import WorkoutExerciseSchema


class WorkoutInSchema(BaseModel):
    date: str
    day: int
    month: int
    year: int


class WorkoutSchema(WorkoutInSchema):
    id: int
    created_at: datetime
    exercises: list[WorkoutExerciseSchema]
    user_id: int
