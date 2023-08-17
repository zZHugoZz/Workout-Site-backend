from fastapi import APIRouter, status
from .. import oauth2
from .. import schemas
from ..models import users
from ..dependencies import common_deps


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=schemas.Profile)
def get_profile(params: common_deps):
    user_id = oauth2.decode_token(params["credentials"].credentials)
    profile = (
        params["db"]
        .query(users.Profile)
        .filter(users.Profile.user_id == user_id)
        .first()
    )
    return profile


@router.put("/", status_code=status.HTTP_200_OK, response_model=schemas.Profile)
async def update_profile(profile: schemas.ProfileIn, params: common_deps):
    return await users.Profile.update_profile(
        params["credentials"], params["db"], profile.model_dump()
    )
