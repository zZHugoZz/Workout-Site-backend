from fastapi import APIRouter, status
from .. import schemas
from ..models import users
from ..dependencies import common_deps


router = APIRouter(prefix="/units", tags=["Units"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Unit)
async def get_unit(params: common_deps):
    return await users.Unit.get_unit(params["credentials"], params["db"])


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Unit)
async def update_unit(unit: schemas.UnitIn, params: common_deps):
    return await users.Unit.update_unit(
        params["credentials"], params["db"], unit.model_dump()
    )
