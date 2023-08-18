from fastapi import APIRouter, status
from .. import schemas
from ..utils import generic_operations
from ..models import performances
from ..dependencies import common_deps


router = APIRouter(prefix="/performances", tags=["Performances"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=schemas.Performance)
async def create_performance(performance: schemas.PerformanceIn, params: common_deps):
    return await generic_operations.create_item(
        params["credentials"], params["db"], performances.Performance, performance
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_performance(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id, params["credentials"], params["db"], performances.Performance, "Performance"
    )
