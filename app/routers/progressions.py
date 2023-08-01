from fastapi import APIRouter, Depends, Security, status, security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import ProgresionIn, Progression
from .. import models
from .authentication import security
from ..utils import create, delete, get_items, get_item


router = APIRouter(prefix="/progressions", tags=["Progressions"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Progression])
def get_progressions(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_items(credentials, db, models.Progression)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Progression)
def get_progression(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_item(id, credentials, db, models.Progression, "Progression")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Progression)
def create_progression(
    progression: ProgresionIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.Progression, progression)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_progression(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.Progression, "Progression")
