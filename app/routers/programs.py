from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import ProgramIn, Program
from .. import models
from .authentication import security
from ..utils import create, delete, get_items, get_item


router = APIRouter(prefix="/programs", tags=["Programs"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Program])
def get_programs(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_items(credentials, db, models.Program)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Program)
def get_program(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return get_item(id, credentials, db, models.Program, "Program")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Program)
def create_program(
    program: ProgramIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.Program, program)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_program(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.Program, "Program")
