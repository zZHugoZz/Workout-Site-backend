from datetime import datetime
from pydantic import BaseModel


class WorkoutExerciseSetInSchema(BaseModel):
    reps: int
    weight: float
    workout_exercise_id: int


class WorkoutExerciseSetSchema(WorkoutExerciseSetInSchema):
    id: int
    created_at: datetime
