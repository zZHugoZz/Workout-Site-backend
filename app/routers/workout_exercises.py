from fastapi import Depends, status, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import WorkoutExercise, WorkoutExerciseIn
from .authentication import security
from ..utils import create, delete, get_item, get_items


router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercises"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[WorkoutExercise])
def get_workout_exercises(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_items(credentials, db, models.WorkoutExercise)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=WorkoutExercise)
def get_workout_exercise(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_item(id, credentials, db, models.WorkoutExercise, "Workout exercise")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkoutExercise)
def create_workout_exercise(
    exercise: WorkoutExerciseIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.WorkoutExercise, exercise)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_workout_exercise(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.WorkoutExercise, "Workout exercise")
