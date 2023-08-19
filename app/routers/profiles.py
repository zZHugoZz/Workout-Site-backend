from fastapi import APIRouter, status
from ..schemas import profiles_schemas
from ..models import profiles
from ..dependencies import common_deps


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=profiles_schemas.ProfileSchema
)
async def get_profile(params: common_deps):
    profile = await profiles.Profile.get_profile(params["credentials"], params["db"])
    return profile


@router.put(
    "/", status_code=status.HTTP_200_OK, response_model=profiles_schemas.ProfileSchema
)
async def update_profile(
    profile: profiles_schemas.ProfileInSchema, params: common_deps
):
    return await profiles.Profile.update_profile(
        params["credentials"], params["db"], profile.model_dump()
    )
