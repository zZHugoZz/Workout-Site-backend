from fastapi import APIRouter, status
from ..schemas import ProgresionIn, Progression
from .. import models
from ..utils import create, delete, get_items, get_item
from ..dependencies import common_deps


router = APIRouter(prefix="/progressions", tags=["Progressions"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Progression])
def get_progressions(params: common_deps):
    return get_items(params["credentials"], params["db"], models.Progression)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Progression)
def get_progression(id: int, params: common_deps):
    return get_item(
        id, params["credentials"], params["db"], models.Progression, "Progression"
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Progression)
def create_progression(progression: ProgresionIn, params: common_deps):
    return create(params["credentials"], params["db"], models.Progression, progression)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_progression(id: int, params: common_deps):
    return delete(
        id, params["credentials"], params["db"], models.Progression, "Progression"
    )
