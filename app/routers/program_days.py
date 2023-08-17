from fastapi import APIRouter, status
from .. import schemas
from .. import models
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/program_days", tags=["Program days"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProgramDay
)
async def create_program_day(program_day: schemas.ProgramDayIn, params: common_deps):
    return await generic_operations.create_item(
        params["credentials"], params["db"], models.ProgramDay, program_day
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_program_day(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id, params["credentials"], params["db"], models.ProgramDay, "Program day"
    )
