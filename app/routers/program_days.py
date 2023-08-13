from fastapi import APIRouter, status
from .. import schemas
from .. import models
from ..utils import create, delete
from ..dependencies import common_deps


router = APIRouter(prefix="/program_days", tags=["Program days"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProgramDay
)
def create_program_day(program_day: schemas.ProgramDayIn, params: common_deps):
    return create(params["credentials"], params["db"], models.ProgramDay, program_day)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program_day(id: int, params: common_deps):
    return delete(
        id, params["credentials"], params["db"], models.ProgramDay, "Program day"
    )
