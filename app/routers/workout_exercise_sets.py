from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..schemas import WorkoutExerciseSet, WorkoutExerciseSetIn
from .authentication import security, get_db
from ..utils import create
from .. import models


router = APIRouter(prefix="/workout_exercise_sets", tags=["Workout exercise sets"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=WorkoutExerciseSet
)
def create_workout_exercise_set(
    workout_exercise_set: WorkoutExerciseSetIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.WorkoutExerciseSet, workout_exercise_set)
