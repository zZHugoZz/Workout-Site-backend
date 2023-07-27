from fastapi import Depends, status, APIRouter, HTTPException, Response, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from .authentication import security
from ..oauth2 import decode_token
from ..utils import FORBIDDEN_EXCEPTION


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
    workout_query = db.query(models.Workout).filter(
        models.Workout.id == exercise.workout_id
    )
    if workout_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    created_exercise = models.WorkoutExercise(**exercise.model_dump())
    db.add(created_exercise)
    db.commit()
    db.refresh(created_exercise)
    return created_exercise


@router.delete("/{workout_id}", status_code=status.HTTP_200_OK)
def delete_workout_exercise(
    workout_exercise_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    workout_exercise_query = db.query(models.WorkoutExercise).filter(
        models.WorkoutExercise.id == workout_exercise_id
    )
    if workout_exercise_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise with id: {workout_exercise_id} doesn't exist",
        )
    workout_query = db.query(models.Workout).filter(
        models.Workout.id == workout_exercise_query.first().workout_id
    )
    if workout_query.first().user_id != user_id:
        return FORBIDDEN_EXCEPTION
    workout_exercise_query.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
