from fastapi import APIRouter, status
from ..schemas import ProgramExerciseIn, ProgramExercise
from .. import models
from ..utils import create, delete
from ..dependencies import common_deps


router = APIRouter(prefix="/program_exercises", tags=["Program Exercises"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProgramExercise)
def create_program_exercise(program_exercise: ProgramExerciseIn, params: common_deps):
    return create(
        params["credentials"], params["db"], models.ProgramExercise, program_exercise
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program_exercise(id: int, params: common_deps):
    return delete(
        id,
        params["credentials"],
        params["db"],
        models.ProgramExercise,
        "Program exercise",
    )
