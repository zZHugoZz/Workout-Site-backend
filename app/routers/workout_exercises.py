from fastapi import status, APIRouter
from .. import models
from ..schemas import WorkoutExercise, WorkoutExerciseIn
from ..utils import create, delete, get_item, get_items
from ..dependencies import common_deps


router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercises"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[WorkoutExercise])
def get_workout_exercises(params: common_deps):
    return get_items(params["credentials"], params["db"], models.WorkoutExercise)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=WorkoutExercise)
def get_workout_exercise(id: int, params: common_deps):
    return get_item(
        id,
        params["credentials"],
        params["db"],
        models.WorkoutExercise,
        "Workout exercise",
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WorkoutExercise)
def create_workout_exercise(exercise: WorkoutExerciseIn, params: common_deps):
    return create(params["credentials"], params["db"], models.WorkoutExercise, exercise)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_workout_exercise(id: int, params: common_deps):
    return delete(
        id,
        params["credentials"],
        params["db"],
        models.WorkoutExercise,
        "Workout exercise",
    )
