from fastapi import APIRouter, Security, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import ProgramExerciseIn, ProgramExercise
from .authentication import security
from .. import models
from ..utils import create, delete


router = APIRouter(prefix="/program_exercises", tags=["Program Exercises"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProgramExercise)
def create_program_exercise(
    program_exercise: ProgramExerciseIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.ProgramExercise, program_exercise)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program_exercise(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.ProgramExercise, "Program exercise")
