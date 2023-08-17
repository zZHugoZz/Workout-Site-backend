from fastapi import APIRouter, status
from .. import schemas
from .. import models
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/progressions", tags=["Progressions"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[schemas.Progression]
)
async def get_progressions(params: common_deps):
    return await generic_operations.get_items(
        params["credentials"], params["db"], models.Progression
    )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Progression)
async def get_progression(id: int, params: common_deps):
    return await generic_operations.get_item(
        id, params["credentials"], params["db"], models.Progression, "Progression"
    )


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.Progression
)
async def create_progression(progression: schemas.ProgresionIn, params: common_deps):
    return await generic_operations.create_item(
        params["credentials"], params["db"], models.Progression, progression
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_progression(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id, params["credentials"], params["db"], models.Progression, "Progression"
    )
