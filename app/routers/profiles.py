from fastapi import APIRouter, status
from .. import oauth2
from .. import schemas
from ..models import users
from ..dependencies import common_deps


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Profile)
async def get_profile(params: common_deps):
    return await users.Profile.get_profile(params["credentials"], params["db"])


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Profile)
async def update_profile(profile: schemas.ProfileIn, params: common_deps):
    return await users.Profile.update_profile(
        params["credentials"], params["db"], profile.model_dump()
    )
