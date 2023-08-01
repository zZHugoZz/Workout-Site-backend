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
    # user_id = decode_token(credentials.credentials)
    # program_day_query = db.query(models.ProgramDay).filter(models.ProgramDay.id == id)
    # if program_day_query.first() is None:
    #     raise NOT_FOUND_EXCEPTION("program day", id)
    # if program_day_query.first().user_id != user_id:
    #     raise FORBIDDEN_EXCEPTION
    # program_day_query.delete()
    # db.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    return delete(id, credentials, db, models.ProgramDay, "Program day")
