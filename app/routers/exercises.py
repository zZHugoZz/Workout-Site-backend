from fastapi import status, APIRouter
from ..models import exercises_model
from ..schemas import exercises_schemas
from ..dependencies import common_deps, Dependencies


router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[exercises_schemas.ExerciseSchema],
)
async def get_exercises(params: common_deps):
    return await exercises_model.Exercise.get_exercises(params[Dependencies.DB])
