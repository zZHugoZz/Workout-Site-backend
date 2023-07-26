from fastapi import Depends, status, APIRouter, HTTPException, Response, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from .authentication import security
from ..oauth2 import decode_token


router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercises"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.WorkoutExercise
)
def create_workout_exercise(
    exercise: schemas.WorkoutExerciseIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    if decode_token(token):
        created_exercise = models.WorkoutExercise(**exercise.model_dump())
        db.add(created_exercise)
        db.commit()
        db.refresh(created_exercise)
        return created_exercise
