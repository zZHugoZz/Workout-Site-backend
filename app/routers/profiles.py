from fastapi import APIRouter, status
from app.oauth2 import decode_token
from ..schemas import Profile, ProfileIn
from .. import models
from ..dependencies import common_deps


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=Profile)
def get_profile(params: common_deps):
    user_id = decode_token(params["credentials"].credentials)
    profile = (
        params["db"]
        .query(models.Profile)
        .filter(models.Profile.user_id == user_id)
        .first()
    )
    return profile


@router.put("/", status_code=status.HTTP_200_OK, response_model=Profile)
def update_profile(profile: ProfileIn, params: common_deps):
    user_id = decode_token(params["credentials"].credentials)
    query = params["db"].query(models.Profile).filter(models.Profile.user_id == user_id)
    query.update(profile.model_dump())
    params["db"].commit()
    return query.first()
