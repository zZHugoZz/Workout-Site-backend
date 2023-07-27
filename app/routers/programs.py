from fastapi import APIRouter, Depends, HTTPException, Response, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from .. import schemas
from .. import models
from .authentication import security


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Program])
def get_programs(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    programs = db.query(models.Program).filter(models.Program.user_id == user_id).all()
    return programs


@router.get(
    "/{program_id}", status_code=status.HTTP_200_OK, response_model=schemas.Program
)
def get_program(
    program_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    workout_query = db.query(models.Program).filter(models.Program.id == program_id)
    if workout_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id: {program_id} doesn't exist",
        )
    if workout_query.first().user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform this action",
        )
    return workout_query.first()


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


@router.delete("/{program_id}", status_code=status.HTTP_200_OK)
def delete_workout(
    program_id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    program_query = db.query(models.Program).filter(models.Program.id == program_id)
    if program_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program with id: {program_id} doesn't exist",
        )
    if program_query.first().user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to perform this action",
        )
    program_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
