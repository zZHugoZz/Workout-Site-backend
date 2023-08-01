from fastapi import APIRouter, Security, Depends, status, Response
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from app.utils import FORBIDDEN_EXCEPTION, NOT_FOUND_EXCEPTION
from .. import schemas
from .authentication import security
from ..models import ProgramExercise
from ..utils import FORBIDDEN_EXCEPTION, NOT_FOUND_EXCEPTION, create


router = APIRouter(prefix="/program_exercises", tags=["Program Exercises"])


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProgramExercise
)
def create_program_exercise(
    program_exercise: schemas.ProgramExerciseIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, ProgramExercise, program_exercise)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program_exercise(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    program_exercise_query = db.query(ProgramExercise).filter(ProgramExercise.id == id)
    if program_exercise_query.first() is None:
        raise NOT_FOUND_EXCEPTION("program exercise", id)
    if program_exercise_query.first().user_id != user_id:
        raise FORBIDDEN_EXCEPTION
    program_exercise_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
