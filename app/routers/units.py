from fastapi import APIRouter, status
from ..schemas import units_schemas
from ..models import units_model
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/units", tags=["Units"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=units_schemas.UnitSchema
)
async def get_unit(params: common_deps):
    return await units_model.Unit.get_unit(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.put(
    "/", status_code=status.HTTP_200_OK, response_model=units_schemas.UnitSchema
)
async def update_unit(unit: units_schemas.UnitInSchema, params: common_deps):
    return await units_model.Unit.update_unit(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB], unit.model_dump()
    )
