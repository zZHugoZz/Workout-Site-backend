from fastapi import status, APIRouter
from ..models import workouts
from .. import schemas
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercises"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[schemas.WorkoutExercise]
)
async def get_workout_exercises(params: common_deps):
    return await generic_operations.get_items(
        params["credentials"], params["db"], workouts.WorkoutExercise
    )


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=schemas.WorkoutExercise
)
async def get_workout_exercise(id: int, params: common_deps):
    return await generic_operations.get_item(
        id,
        params["credentials"],
        params["db"],
        workouts.WorkoutExercise,
        "Workout exercise",
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.WorkoutExercise
)
async def create_workout_exercise(
    exercise: schemas.WorkoutExerciseIn, params: common_deps
):
    return await generic_operations.create_item(
        params["credentials"], params["db"], workouts.WorkoutExercise, exercise
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_workout_exercise(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params["credentials"],
        params["db"],
        workouts.WorkoutExercise,
        "Workout exercise",
    )
