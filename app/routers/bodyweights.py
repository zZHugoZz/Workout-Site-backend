from fastapi import APIRouter, status
from .. import schemas
from ..utils import generic_operations
from ..models import bodyweights
from datetime import date
from ..dependencies import common_deps


router = APIRouter(prefix="/bodyweights", tags=["Body weights"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.BodyWeight
)
async def create_bodyweight(bodyweight: schemas.BodyWeightIn, params: common_deps):
    current_date = {"date": str(date.today())}
    return await generic_operations.create_item(
        params["credentials"],
        params["db"],
        bodyweights.BodyWeight,
        bodyweight,
        current_date,
    )


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[schemas.BodyWeight]
)
async def get_bodyweights(params: common_deps):
    return await generic_operations.get_items(
        params["credentials"], params["db"], models.BodyWeight
    )
