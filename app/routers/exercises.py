from fastapi import Depends, Query, status, APIRouter, HTTPException, Security
from typing import Annotated
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import Exercise

from .authentication import security
from ..oauth2 import decode_token
from fastapi.security import HTTPAuthorizationCredentials


router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Exercise])
def search_exercises(
    credentials: HTTPAuthorizationCredentials = Security(security),
    q: Annotated[str | None, Query(max_length=100)] = None,
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    if decode_token(token):
        exercises = (
            db.query(models.Exercise).filter(models.Exercise.name.contains(q)).all()
        )
        if q == "":
            exercises = []
        return exercises


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Exercise])
def get_exercises(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    exercises = db.query(models.Exercise).all()
    return exercises
