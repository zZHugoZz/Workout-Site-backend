from fastapi import APIRouter, status
from ..schemas import programs_schemas
from ..models import programs
from ..utils import generic_operations
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[programs_schemas.ProgramSchema],
)
async def get_programs(params: common_deps):
    return await generic_operations.get_items(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB], programs.Program
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=programs_schemas.ProgramSchema,
)
async def get_program(id: int, params: common_deps):
    return await generic_operations.get_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        programs.Program,
        "Program",
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=programs_schemas.ProgramSchema,
)
async def create_program(
    program: programs_schemas.ProgramInSchema, params: common_deps
):
    return await generic_operations.create_item(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        programs.Program,
        program,
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_program(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        programs.Program,
        "Program",
    )
