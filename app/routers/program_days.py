from fastapi import APIRouter, status
from ..schemas import program_days_schemas
from ..models import program_days_model
from ..utils import generic_operations
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/program_days", tags=["Program days"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=program_days_schemas.ProgramDaySchema,
)
async def create_program_day(
    program_day: program_days_schemas.ProgramDayInSchema, params: common_deps
):
    return await generic_operations.create_item(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        program_days_model.ProgramDay,
        program_day,
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_program_day(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        program_days_model.ProgramDay,
        "Program day",
    )
