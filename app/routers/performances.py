from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import Performance, PerformanceIn
from .authentication import security
from ..utils import create, delete
from .. import models


router = APIRouter(prefix="/performances", tags=["Performances"])


@router.post("/", status_code=status.HTTP_200_OK, response_model=Performance)
def create_performance(
    performance: PerformanceIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return create(credentials, db, models.Performance, performance)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_performance(
    id: int,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return delete(id, credentials, db, models.Performance, "Performance")
