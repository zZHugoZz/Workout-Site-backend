from fastapi import APIRouter, status
from ..schemas import bodyweights_schemas
from ..utils import generic_operations
from ..models import bodyweights_model
from datetime import date
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/bodyweights", tags=["Body weights"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=bodyweights_schemas.BodyWeightSchema,
)
async def create_bodyweight(
    bodyweight_in: bodyweights_schemas.BodyWeightInSchema, params: common_deps
):
    # current_date = {"date": date.today()}
    # return await generic_operations.create_item(
    #     params[Dependencies.CREDENTIALS],
    #     params[Dependencies.DB],
    #     bodyweights_model.BodyWeight,
    #     bodyweight,
    #     current_date,
    # )
    return await bodyweights_model.BodyWeight.add_bodyweight(
        str(date.today()),
        bodyweight_in,
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[bodyweights_schemas.BodyWeightSchema],
)
async def get_bodyweights(params: common_deps):
    return await generic_operations.get_items(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        bodyweights_model.BodyWeight,
    )
