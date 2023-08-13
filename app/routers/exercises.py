from fastapi import status, APIRouter
from .. import models
from ..schemas import Exercise
from ..dependencies import common_deps


router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Exercise])
def get_exercises(params: common_deps):
    exercises = params["db"].query(models.Exercise).all()
    return exercises
