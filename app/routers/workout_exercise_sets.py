from fastapi import APIRouter, status
from ..schemas import workout_exercise_sets_schemas
from ..utils import generic_operations
from ..models import workout_exercise_sets
from ..dependencies import common_deps


router = APIRouter(prefix="/workout_exercise_sets", tags=["Workout exercise sets"])


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=workout_exercise_sets_schemas.WorkoutExerciseSetSchema,
)
async def get_workout_exercise_set(id: int, params: common_deps):
    return await generic_operations.get_item(
        id,
        params["credentials"],
        params["db"],
        workout_exercise_sets.WorkoutExerciseSet,
        "Workout exercise set",
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=workout_exercise_sets_schemas.WorkoutExerciseSetSchema,
)
async def create_workout_exercise_set(
    workout_exercise_set: workout_exercise_sets_schemas.WorkoutExerciseSetInSchema,
    params: common_deps,
):
    return await generic_operations.create_item(
        params["credentials"],
        params["db"],
        workout_exercise_sets.WorkoutExerciseSet,
        workout_exercise_set,
    )


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=workout_exercise_sets_schemas.WorkoutExerciseSetSchema,
)
async def delete_workout_exercise_set(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params["credentials"],
        params["db"],
        workout_exercise_sets.WorkoutExerciseSet,
        "Workout exercise set",
    )
