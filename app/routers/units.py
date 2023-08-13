from fastapi import APIRouter, status
from app.oauth2 import decode_token
from ..schemas import Unit, UnitIn
from .. import models
from ..dependencies import common_deps


router = APIRouter(prefix="/units", tags=["Units"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=Unit)
def get_unit(params: common_deps):
    user_id = decode_token(params["credentials"].credentials)
    unit = (
        params["db"].query(models.Unit).filter(models.Unit.user_id == user_id).first()
    )
    return unit


@router.put("/", status_code=status.HTTP_200_OK, response_model=Unit)
def update_unit(unit: UnitIn, params: common_deps):
    user_id = decode_token(params["credentials"].credentials)
    query = params["db"].query(models.Unit).filter(models.Unit.user_id == user_id)
    query.update(unit.model_dump())
    params["db"].commit()
    return query.first()
