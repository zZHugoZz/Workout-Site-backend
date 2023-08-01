from fastapi import APIRouter, Depends, Security, status, security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from ..schemas import ProgresionIn, Progression
from .. import models
from .authentication import security
from ..utils import create, delete


router = APIRouter(prefix="/progressions", tags=["Progressions"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Progression])
def get_progressions(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    progressions = (
        db.query(models.Progression).filter(models.Progression.user_id == user_id).all()
    )
    return progressions


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Progression)
def get_progression(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    pass


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
