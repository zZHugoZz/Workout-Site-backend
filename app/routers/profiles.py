from fastapi import APIRouter, status

from app.utils import generic_operations
from ..schemas import profiles_schemas
from ..models import profiles_model
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=profiles_schemas.ProfileSchema
)
async def get_profile(params: common_deps):
    return await generic_operations.get_item(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        profiles_model.Profile,
        "Profile",
    )


@router.put(
    "/", status_code=status.HTTP_200_OK, response_model=profiles_schemas.ProfileSchema
)
async def update_profile(
    profile: profiles_schemas.ProfileInSchema, params: common_deps
):
    return await profiles_model.Profile.update_profile(
        params[Dependencies.CREDENTIALS],
        params[Dependencies.DB],
        profile.model_dump(exclude_unset=True),
    )
