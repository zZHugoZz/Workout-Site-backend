from fastapi import APIRouter, status
from ..schemas import WorkoutExerciseSet, WorkoutExerciseSetIn
from ..utils import create, get_item, delete
from .. import models
from ..dependencies import common_deps


router = APIRouter(prefix="/workout_exercise_sets", tags=["Workout exercise sets"])


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=WorkoutExerciseSet)
def get_workout_exercise_set(id: int, params: common_deps):
    return get_item(
        id,
        params["credentials"],
        params["db"],
        models.WorkoutExerciseSet,
        "Workout exercise set",
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=WorkoutExerciseSet
)
def create_workout_exercise_set(
    workout_exercise_set: WorkoutExerciseSetIn, params: common_deps
):
    return create(
        params["credentials"],
        params["db"],
        models.WorkoutExerciseSet,
        workout_exercise_set,
    )


@router.delete(
    "/{id}", status_code=status.HTTP_200_OK, response_model=WorkoutExerciseSet
)
def delete_workout_exercise_set(id: int, params: common_deps):
    return delete(
        id,
        params["credentials"],
        params["db"],
        models.WorkoutExerciseSet,
        "Workout exercise set",
    )
