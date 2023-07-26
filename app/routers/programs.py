from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from .. import schemas
from .. import models
from .authentication import security


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Program)
def create_program(
    program: schemas.ProgramIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    created_program = models.Program(**program.model_dump(), user_id=user_id)
    db.add(created_program)
    db.commit()
    db.refresh(created_program)
    return created_program
