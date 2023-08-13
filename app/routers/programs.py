from fastapi import APIRouter, status
from ..schemas import ProgramIn, Program
from .. import models
from ..utils import create, delete, get_items, get_item
from ..dependencies import common_deps


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Program])
def get_programs(params: common_deps):
    return get_items(params["credentials"], params["db"], models.Program)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Program)
def get_program(id: int, params: common_deps):
    return get_item(id, params["credentials"], params["db"], models.Program, "Program")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Program)
def create_program(program: ProgramIn, params: common_deps):
    return create(params["credentials"], params["db"], models.Program, program)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program(id: int, params: common_deps):
    return delete(id, params["credentials"], params["db"], models.Program, "Program")
