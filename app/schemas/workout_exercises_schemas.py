from typing import Optional
from pydantic import BaseModel
from .workout_exercise_sets_schemas import WorkoutExerciseSetSchema


class WorkoutExerciseInSchema(BaseModel):
    name: str
    n_sets: Optional[int]
    workout_id: int


class WorkoutExerciseSchema(WorkoutExerciseInSchema):
    id: int
    sets: list[WorkoutExerciseSetSchema]
