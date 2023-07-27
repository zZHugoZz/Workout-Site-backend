from fastapi import APIRouter, Depends, HTTPException, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from .. import schemas
from .authentication import security
from .. import models
from ..utils import FORBIDDEN_EXCEPTION, NOT_FOUND_EXCEPTION


router = APIRouter(prefix="/program_days", tags=["Program days"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProgramDay
)
def create_program_day(
    program_day: schemas.ProgramDayIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    created_program_day = models.ProgramDay(**program_day.model_dump(), user_id=user_id)
    db.add(created_program_day)
    db.commit()
    db.refresh(created_program_day)
    return created_program_day


@router.delete("/{program_day_id}", status_code=status.HTTP_200_OK)
def delete_program_day(
    program_day_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    program_day_query = db.query(models.ProgramDay).filter(
        models.ProgramDay.id == program_day_id
    )
    if program_day_query.first() is None:
        raise NOT_FOUND_EXCEPTION("program day", program_day_id)
    if program_day_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    program_day_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
