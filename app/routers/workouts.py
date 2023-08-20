from fastapi import status, APIRouter
from ..models import workouts
from ..schemas import workouts_schemas
from datetime import date
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


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=workouts_schemas.WorkoutSchema,
)
async def create_workout(params: common_deps):
    # additional_data = {"date": str(date.today())}
    # return await generic_operations.create_item(
    #     params[Dependencies.CREDENTIALS],
    #     params[Dependencies.DB],
    #     workouts.Workout,
    #     additional_data=additional_data,
    # )
    return await workouts.Workout.create_workout(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_workout(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        workouts.Workout,
        "Workout",
    )
