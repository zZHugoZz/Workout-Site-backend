from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from .. import schemas
from .authentication import security
from .. import models
from ..utils import create, delete


router = APIRouter(prefix="/program_days", tags=["Program days"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProgramDay
)
def create_program_day(
    program_day: schemas.ProgramDayIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.ProgramDay, program_day)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program_day(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.ProgramDay, "Program day")
