from datetime import datetime
from pydantic import BaseModel
from .workout_exercises_schemas import WorkoutExerciseSchema


class WorkoutSchema(BaseModel):
    id: int
    date: str
    day: int
    month: int
    year: int
    created_at: datetime
    user_id: int
    exercises: list[WorkoutExerciseSchema]
