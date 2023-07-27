from fastapi import Depends, status, APIRouter, Response, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from .authentication import security
from ..oauth2 import decode_token
from ..utils import FORBIDDEN_EXCEPTION, NOT_FOUND_EXCEPTION


router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercises"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.WorkoutExercise
)
def create_workout_exercise(
    exercise: schemas.WorkoutExerciseIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    created_exercise = models.WorkoutExercise(**exercise.model_dump(), user_id=user_id)
    db.add(created_exercise)
    db.commit()
    db.refresh(created_exercise)
    return created_exercise


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_workout_exercise(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    workout_exercise_query = db.query(models.WorkoutExercise).filter(
        models.WorkoutExercise.id == id
    )
    if workout_exercise_query.first() is None:
        raise NOT_FOUND_EXCEPTION("workout exercise", id)
    if workout_exercise_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    workout_exercise_query.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
