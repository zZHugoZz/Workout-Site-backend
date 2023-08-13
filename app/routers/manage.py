from fastapi import status, APIRouter
from .. import models
from ..schemas import ManageData
from ..utils import decode_token
from ..dependencies import common_deps


router = APIRouter(prefix="/manage", tags=["Manage"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=ManageData)
def get_manage_data(params: common_deps):
    user_id = decode_token(params["credentials"].credentials)
    workouts = (
        params["db"]
        .query(models.Workout)
        .filter(models.Workout.user_id == user_id)
        .all()
    )
    programs = (
        params["db"]
        .query(models.Program)
        .filter(models.Program.user_id == user_id)
        .all()
    )
    progressions = (
        params["db"]
        .query(models.Progression)
        .filter(models.Progression.user_id == user_id)
        .all()
    )
    unit = (
        params["db"].query(models.Unit).filter(models.Unit.user_id == user_id).first()
    )
    return {
        "workouts": workouts,
        "programs": programs,
        "progressions": progressions,
        "unit": unit,
    }
