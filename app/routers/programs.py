from fastapi import APIRouter, status
from .. import schemas
from .. import models
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Program])
async def get_programs(params: common_deps):
    return await generic_operations.get_items(
        params["credentials"], params["db"], models.Program
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Program)
async def get_program(id: int, params: common_deps):
    return await generic_operations.get_item(
        id, params["credentials"], params["db"], models.Program, "Program"
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Program)
async def create_program(program: schemas.ProgramIn, params: common_deps):
    return await generic_operations.create_item(
        params["credentials"], params["db"], models.Program, program
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_program(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id, params["credentials"], params["db"], models.Program, "Program"
    )
