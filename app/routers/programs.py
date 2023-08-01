from fastapi import APIRouter, Depends, Response, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from .. import schemas
from .. import models
from .authentication import security
from ..utils import FORBIDDEN_EXCEPTION, NOT_FOUND_EXCEPTION, create


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Program])
def get_programs(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    programs = db.query(models.Program).filter(models.Program.user_id == user_id).all()
    return programs


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Program)
def get_program(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    workout_query = db.query(models.Program).filter(models.Program.id == id)
    if workout_query.first() is None:
        raise NOT_FOUND_EXCEPTION("program", id)
    if workout_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    return workout_query.first()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Program)
def create_program(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.Program)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    program_query = db.query(models.Program).filter(models.Program.id == id)
    if program_query.first() is None:
        raise NOT_FOUND_EXCEPTION("program", id)
    if program_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    program_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
