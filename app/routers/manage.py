from fastapi import status, APIRouter
from ..models.programs_model import Program
from ..models.progressions_model import Progression
from ..models import units_model, workouts_model
from ..schemas import manage_data_schemas
from ..utils import generic_operations
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/manage", tags=["Manage"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=manage_data_schemas.ManageDataSchema,
)
async def get_manage_data(params: common_deps):
    todays_workout = await workouts_model.Workout.get_workout_by_current_date(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )
    programs = await generic_operations.get_items(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB], Program
    )
    progressions = await generic_operations.get_items(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB], Progression
    )
    unit = await units_model.Unit.get_unit(
        params[Dependencies.CREDENTIALS], params[Dependencies.DB]
    )
    return {
        "todays_workout": todays_workout,
        "programs": programs,
        "progressions": progressions,
        "unit": unit,
    }
