from fastapi import Depends, status, APIRouter, HTTPException, Response
from typing import Annotated
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from ..oauth2 import get_current_user


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Workout])
def get_workouts(
    current_user: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    workouts = (
        db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()
    )
    print(workouts)
    return workouts


@router.get(
    "/{workout_id}", status_code=status.HTTP_200_OK, response_model=schemas.Workout
)
def get_workout(
    workout_id: int,
    current_user: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    workout_query = db.query(models.Workout).filter(models.Workout.id == workout_id)
    if workout_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with id: {workout_id} doesn't exist",
        )
    if current_user.id != workout_query.first().user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unhauthorized to perform this action",
        )
    return workout_query.first()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Workout)
def create_workout(
    current_user: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    created_workout = models.Workout(user_id=current_user.id)
    db.add(created_workout)
    db.commit()
    db.refresh(created_workout)
    return created_workout


@router.delete("/{workout_id}", status_code=status.HTTP_200_OK)
def delete_workout(
    workout_id: int,
    current_user: Annotated[int, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    workout_query = db.query(models.Workout).filter(models.Workout.id == workout_id)
    if workout_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Workout with id: {workout_id} doesn't exist",
        )
    if current_user.id != workout_query.first().user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unhauthorized to perform this action",
        )
    workout_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
