from fastapi import APIRouter, status
from ..schemas import profiles_schemas
from ..models import profiles
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=profiles_schemas.ProfileSchema
)
async def get_profile(params: common_deps):
    return await profiles.Profile.get_profile(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )


@router.put(
    "/", status_code=status.HTTP_200_OK, response_model=profiles_schemas.ProfileSchema
)
async def update_profile(
    profile: profiles_schemas.ProfileInSchema, params: common_deps
):
    return await profiles.Profile.update_profile(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB], profile.model_dump()
    )
