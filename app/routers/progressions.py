from fastapi import APIRouter, Depends, Security, status, security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from ..schemas import ProgresionIn, Progression
from .. import models
from .authentication import security

from ..utils import create


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


# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=Progression)
# def create_progression(
#     progression: ProgresionIn,
#     credentials: HTTPAuthorizationCredentials = Security(security),
#     db: Session = Depends(get_db),
# ):
#     user_id = decode_token(credentials.credentials)
#     created_progression = models.Progression(
#         **progression.model_dump(), user_id=user_id
#     )
#     db.add(created_progression)
#     db.commit()
#     db.refresh(created_progression)
#     return created_progression


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Progression)
def create_progression(
    progression: ProgresionIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(
        data=progression, credentials=credentials, db=db, model=models.Progression
    )
