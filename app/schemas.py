from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


# -------------------- users --------------------
class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: EmailStr


class UserIn(BaseUser):
    password: str


class UserOut(BaseUser):
    id: int
    created_at: datetime


class ProfileIn(BaseModel):
    age: int | None = None
    gender: str | None = None
    profile_picture: bytes | None = None


class Profile(ProfileIn):
    user_id: int
    user: UserOut


# -------------------- tokens --------------------
class Token(BaseModel):
    access_token: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: int


class RefreshToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    refresh_token: str


# -------------------- explore exercises --------------------
class Exercise(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    link: str


# -------------------- workouts --------------------
class WorkoutExerciseSetIn(BaseModel):
    reps: int
    weight: float
    workout_exercise_id: int


class WorkoutExerciseSet(WorkoutExerciseSetIn):
    id: int
    created_at: datetime


class WorkoutExerciseIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    n_sets: int
    workout_id: int


class WorkoutExercise(WorkoutExerciseIn):
    id: int
    sets: list[WorkoutExerciseSet]


class Workout(BaseModel):
    id: int
    date: str
    created_at: datetime
    user_id: int
    user: UserOut
    exercises: list[WorkoutExercise]


# -------------------- programs --------------------
class ProgramExerciseIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    min_sets: int
    max_sets: int
    min_reps: int
    max_reps: int
    day_id: int


class ProgramExercise(ProgramExerciseIn):
    id: int


class ProgramDayIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    program_id: int


class ProgramDay(ProgramDayIn):
    id: int
    exercises: list[ProgramExercise]


class ProgramIn(BaseModel):
    name: str
    description: str
    n_days: int


class Program(ProgramIn):
    id: int
    user_id: int
    days: list[ProgramDay]
    created_at: datetime


# -------------------- progressions --------------------
class PerformanceIn(BaseModel):
    date: str
    weight: float
    progression_id: int


class Performance(PerformanceIn):
    id: int
    created_at: datetime
    user_id: int


class ProgresionIn(BaseModel):
    name: str
    color: str


class Progression(ProgresionIn):
    id: int
    created_at: datetime
    user_id: int
    performances: list[Performance]


class UnitIn(BaseModel):
    unit: str


class Unit(UnitIn):
    id: int
    user_id: int


# -------------------- weight changes --------------------
class BodyWeightIn(BaseModel):
    weight: float


class BodyWeight(BodyWeightIn):
    id: int
    user_id: int
    date: str
    created_at: datetime


class BodyWeightUnitIn(BaseModel):
    unit: str


class BodyWeightUnit(BodyWeightUnitIn):
    id: int
    user_id: int
