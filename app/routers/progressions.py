from fastapi import APIRouter, status
from ..schemas import progressions_schemas
from ..models import progressions
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/progressions", tags=["Progressions"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[progressions_schemas.ProgressionSchema],
)
async def get_progressions(params: common_deps):
    return await generic_operations.get_items(
        params["credentials"], params["db"], progressions.Progression
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=progressions_schemas.ProgressionSchema,
)
async def get_progression(id: int, params: common_deps):
    return await generic_operations.get_item(
        id, params["credentials"], params["db"], progressions.Progression, "Progression"
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=progressions_schemas.ProgressionSchema,
)
async def create_progression(
    progression: progressions_schemas.ProgresionInSchema, params: common_deps
):
    return await generic_operations.create_item(
        params["credentials"], params["db"], progressions.Progression, progression
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_progression(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id, params["credentials"], params["db"], progressions.Progression, "Progression"
    )
