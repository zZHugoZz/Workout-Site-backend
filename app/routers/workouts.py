from fastapi import Depends, status, APIRouter, HTTPException, Response, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from .authentication import security
from ..oauth2 import decode_token


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Workout])
def get_workouts(
    db: Session = Depends(get_db),
):
    workouts = db.query(models.Workout).all()
    print(workouts)
    return workouts


@router.get(
    "/{workout_id}", status_code=status.HTTP_200_OK, response_model=schemas.Workout
)
def get_workout(
    workout_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    if decode_token(token):
        print(decode_token(token))
        workout_query = db.query(models.Workout).filter(models.Workout.id == workout_id)
        if workout_query.first() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Workout with id: {workout_id} doesn't exist",
            )
        return workout_query.first()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Workout)
def create_workout(
    db: Session = Depends(get_db),
):
    created_workout = models.Workout()
    db.add(created_workout)
    db.commit()
    db.refresh(created_workout)
    return created_workout


@router.delete("/{workout_id}", status_code=status.HTTP_200_OK)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
):
    workout_query = db.query(models.Workout).filter(models.Workout.id == workout_id)
    if workout_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with id: {workout_id} doesn't exist",
        )
    workout_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
