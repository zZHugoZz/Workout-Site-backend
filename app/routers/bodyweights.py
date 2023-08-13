from fastapi import APIRouter, status
from ..schemas import BodyWeight, BodyWeightIn
from ..utils import create, get_items
from .. import models
from datetime import date
from ..dependencies import common_deps


router = APIRouter(prefix="/bodyweights", tags=["Body weights"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BodyWeight)
def create_bodyweight(bodyweight: BodyWeightIn, params: common_deps):
    current_date = {"date": date.today()}
    return create(
        params["credentials"], params["db"], models.BodyWeight, bodyweight, current_date
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[BodyWeight])
def get_bodyweights(params: common_deps):
    return get_items(params["credentials"], params["db"], models.BodyWeight)
