from fastapi import status, APIRouter
from ..models.workouts import Workout
from ..models.programs import Program
from ..models.progressions import Progression
from ..models import units
from ..schemas import manage_data_schemas
from ..utils import generic_operations
from ..dependencies import common_deps


router = APIRouter(prefix="/manage", tags=["Manage"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=manage_data_schemas.ManageDataSchema,
)
async def get_manage_data(params: common_deps):
    workouts = await generic_operations.get_items(
        params["credentials"], params["db"], Workout
    )
    programs = await generic_operations.get_items(
        params["credentials"], params["db"], Program
    )
    progressions = await generic_operations.get_items(
        params["credentials"], params["db"], Progression
    )
    unit = await units.Unit.get_unit(params["credentials"], params["db"])
    # workouts = (
    #     params["db"]
    #     .query(models.Workout)
    #     .filter(models.Workout.user_id == user_id)
    #     .all()
    # )
    # programs = (
    #     params["db"]
    #     .query(models.Program)
    #     .filter(models.Program.user_id == user_id)
    #     .all()
    # )
    # progressions = (
    #     params["db"]
    #     .query(models.Progression)
    #     .filter(models.Progression.user_id == user_id)
    #     .all()
    # )
    # unit = (
    #     params["db"].query(models.Unit).filter(models.Unit.user_id == user_id).first()
    # )
    return {
        "workouts": workouts,
        "programs": programs,
        "progressions": progressions,
        "unit": unit,
    }
