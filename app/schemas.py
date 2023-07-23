from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    id: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class Exercise(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    link: str


class WorkoutExercise(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    n_sets: int
    n_reps: int
    weight: float
    unit: str
    workout_id: int


class Workout(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    exercises: list[WorkoutExercise]
