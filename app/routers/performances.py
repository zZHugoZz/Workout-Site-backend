from fastapi import APIRouter, status
from ..schemas import Performance, PerformanceIn
from ..utils import create, delete
from .. import models
from ..dependencies import common_deps


router = APIRouter(prefix="/performances", tags=["Performances"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=Performance)
def create_performance(performance: PerformanceIn, params: common_deps):
    return create(params["credentials"], params["db"], models.Performance, performance)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_performance(id: int, params: common_deps):
    return delete(
        id, params["credentials"], params["db"], models.Performance, "Performance"
    )
