from fastapi import APIRouter, status
from ..schemas import program_exercises_schemas
from ..models import program_exercises
from ..utils import generic_operations
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/program_exercises", tags=["Program Exercises"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=program_exercises_schemas.ProgramExerciseSchema,
)
async def create_program_exercise(
    program_exercise: program_exercises_schemas.ProgramExerciseInSchema,
    params: common_deps,
):
    return await generic_operations.create_item(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        program_exercises.ProgramExercise,
        program_exercise,
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_program_exercise(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        program_exercises.ProgramExercise,
        "Program exercise",
    )
