from fastapi import APIRouter, status
from .. import schemas
from ..models import programs
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/program_exercises", tags=["Program Exercises"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProgramExercise
)
async def create_program_exercise(
    program_exercise: schemas.ProgramExerciseIn, params: common_deps
):
    return await generic_operations.create_item(
        params["credentials"], params["db"], programs.ProgramExercise, program_exercise
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_program_exercise(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params["credentials"],
        params["db"],
        programs.ProgramExercise,
        "Program exercise",
    )
