from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from .. import schemas
from .authentication import security
from .. import models


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
    program_id = db.query(models.Program).filter(
        models.Program.id == program_day.program_id
    )
    if program_id.first().user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform this action",
        )
    created_program_day = models.ProgramDay(**program_day.model_dump())
    db.add(created_program_day)
    db.commit()
    db.refresh(created_program_day)
    return created_program_day
