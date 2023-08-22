from typing import Annotated
from fastapi import Query, status, APIRouter
from ..models import workouts
from ..schemas import workouts_schemas
from ..utils import generic_operations
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[workouts_schemas.WorkoutSchema],
)
async def get_workouts(params: common_deps):
    return await generic_operations.get_items(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB], workouts.Workout
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=workouts_schemas.WorkoutSchema,
)
async def get_workout(id: int, params: common_deps):
    return await generic_operations.get_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        workouts.Workout,
        "Workout",
    )


@router.get("/filter/", status_code=status.HTTP_200_OK)
async def get_workouts_by_month(
    month: Annotated[int, Query()], year: Annotated[int, Query()], params: common_deps
):
    return await workouts.Workout.get_workouts_by_month(
        month, year, params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.get(
    "/workout_by_date/",
    status_code=status.HTTP_200_OK,
    response_model=workouts_schemas.WorkoutSchema | None,
)
async def get_workout_by_date(date: Annotated[str, Query()], params: common_deps):
    return await workouts.Workout.get_workout_by_date(
        date, params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


# Not really necessary, mostly for testing, already used in manage.py
@router.get(
    "/workout_by_current_date/",
    status_code=status.HTTP_200_OK,
    response_model=workouts_schemas.WorkoutSchema | None,
)
async def get_workout_by_current_date(params: common_deps):
    return await workouts.Workout.get_workout_by_current_date(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=workouts_schemas.WorkoutSchema,
)
async def create_workout(
    workout: workouts_schemas.WorkoutInSchema, params: common_deps
):
    return await generic_operations.create_item(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        workouts.Workout,
        workout,
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_workout(id: int, params: common_deps):
    # return await generic_operations.delete_item(
    #     id,
    #     params[Dependencies.CREDENTIALS],
    #     params[Dependencies.DB],
    #     workouts.Workout,
    #     "Workout",
    # )
    return await workouts.Workout.delete_workout(
        id, params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )
