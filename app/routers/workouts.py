from fastapi import status, APIRouter
from .. import models
from ..schemas import Workout
from datetime import date
from ..utils import create, delete, get_items, get_item
from ..dependencies import common_deps


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Workout])
def get_workouts(params: common_deps):
    return get_items(params["credentials"], params["db"], models.Workout)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Workout)
def get_workout(id: int, params: common_deps):
    return get_item(id, params["credentials"], params["db"], models.Workout, "Workout")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Workout)
def create_workout(params: common_deps):
    additional_data = {"date": date.today()}
    return create(
        params["credentials"],
        params["db"],
        models.Workout,
        additional_data=additional_data,
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_workout(id: int, params: common_deps):
    return delete(id, params["credentials"], params["db"], models.Workout, "Workout")
