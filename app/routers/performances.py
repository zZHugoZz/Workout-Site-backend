from fastapi import APIRouter, status
from ..schemas import performances_schemas
from ..utils import generic_operations
from ..models import performances_model
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/performances", tags=["Performances"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=performances_schemas.PerformanceSchema,
)
async def create_performance(
    performance_in: performances_schemas.PerformanceInSchema, params: common_deps
):
    # return await generic_operations.create_item(
    #     params[Dependencies.CREDENTIALS],
    #     params[Dependencies.DB],
    #     performances.Performance,
    #     performance,
    # )
    return await performances_model.Performance.add_performance(
        performance_in, params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_performance(id: int, params: common_deps):
    return await generic_operations.delete_item(
        id,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        performances_model.Performance,
        "Performance",
    )
