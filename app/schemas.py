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
    refresh_token: str


class TokenData(BaseModel):
    user_id: int


class RefreshToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    refresh_token: str


class Exercise(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    link: str


class WorkoutExercise(BaseModel):
    id: int
    name: str
    sets: int
    reps: int
    weight: float
    unit: str
    workout_id: int


class WorkoutExerciseIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    sets: int
    reps: int
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


class ProgramExercise(BaseModel):
    id: int | None = None
    name: str
    min_sets: int
    max_sets: int
    min_reps: int
    max_reps: int
    day_id: int


class ProgramDay(BaseModel):
    id: int
    program_id: int
    exercises: list[ProgramExercise]


class ProgramIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class Program(BaseModel):
    id: int
    name: str
    user_id: int
    days: list[ProgramDay]
    created_at: datetime
