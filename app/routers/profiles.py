from fastapi import APIRouter, status
from .. import schemas
from ..models import profiles
from ..dependencies import common_deps


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Profile)
async def get_profile(params: common_deps):
    return await profiles.Profile.get_profile(params["credentials"], params["db"])


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Profile)
async def update_profile(profile: schemas.ProfileIn, params: common_deps):
    return await profiles.Profile.update_profile(
        params["credentials"], params["db"], profile.model_dump()
    )
