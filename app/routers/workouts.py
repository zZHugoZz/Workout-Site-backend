from fastapi import status, APIRouter
from ..models import workouts
from .. import schemas
from datetime import date
from ..utils import create, delete, get_items, get_item
from ..dependencies import common_deps


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Workout])
async def get_workouts(params: common_deps):
    return await get_items(params["credentials"], params["db"], workouts.Workout)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Workout)
async def get_workout(id: int, params: common_deps):
    return await get_item(
        id, params["credentials"], params["db"], workouts.Workout, "Workout"
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Workout)
async def create_workout(params: common_deps):
    additional_data = {"date": str(date.today())}
    return await create(
        params["credentials"],
        params["db"],
        workouts.Workout,
        additional_data=additional_data,
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_workout(id: int, params: common_deps):
    return await delete(
        id, params["credentials"], params["db"], workouts.Workout, "Workout"
    )
