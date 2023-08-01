from fastapi import Depends, status, APIRouter, Response, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from .authentication import security
from ..oauth2 import decode_token
from ..utils import FORBIDDEN_EXCEPTION, NOT_FOUND_EXCEPTION
from datetime import date
from ..utils import create, delete, get_items, get_item


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Workout])
def get_workouts(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    # user_id = decode_token(credentials.credentials)
    # workouts = db.query(models.Workout).filter(models.Workout.user_id == user_id).all()
    # return workouts
    return get_items(credentials, db, models.Workout)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Workout)
def get_workout(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    workout_query = db.query(models.Workout).filter(models.Workout.id == id)
    if workout_query.first() is None:
        raise NOT_FOUND_EXCEPTION("workout", id)
    if workout_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    return workout_query.first()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Workout)
def create_workout(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    current_date = {"date": date.today()}
    return create(credentials, db, models.Workout, additional_data=current_date)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_workout(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.Workout, "Workout")
