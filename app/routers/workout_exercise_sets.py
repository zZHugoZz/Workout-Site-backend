from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from ..schemas import WorkoutExerciseSet, WorkoutExerciseSetIn
from .authentication import security, get_db
from ..utils import create, get_item, delete
from .. import models


router = APIRouter(prefix="/workout_exercise_sets", tags=["Workout exercise sets"])


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=WorkoutExerciseSet)
def get_workout_exercise_set(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_item(
        id, credentials, db, models.WorkoutExerciseSet, "Workout exercise set"
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=WorkoutExerciseSet
)
def create_workout_exercise_set(
    workout_exercise_set: WorkoutExerciseSetIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.WorkoutExerciseSet, workout_exercise_set)


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, response_model=WorkoutExerciseSet
)
def delete_workout_exercise_set(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(
        id, credentials, db, models.WorkoutExerciseSet, "Workout exercise set"
    )
