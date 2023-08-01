from fastapi import Depends, status, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from .authentication import security
from ..utils import create, delete


router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercises"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.WorkoutExercise
)
def create_workout_exercise(
    exercise: schemas.WorkoutExerciseIn,
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
