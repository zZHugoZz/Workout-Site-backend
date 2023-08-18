from datetime import datetime
from pydantic import BaseModel
from .workout_exercises_schemas import WorkoutExerciseSchema


class WorkoutSchema(BaseModel):
    id: int
    date: str
    created_at: datetime
    user_id: int
    exercises: list[WorkoutExerciseSchema]
