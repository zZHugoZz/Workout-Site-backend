from fastapi import Depends, status, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import Workout
from .authentication import security
from datetime import date
from ..utils import create, delete, get_items, get_item


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Workout])
def get_workouts(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_items(credentials, db, models.Workout)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Workout)
def get_workout(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_item(id, credentials, db, models.Workout, "Workout")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Workout)
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
