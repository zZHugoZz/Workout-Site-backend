from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from ..schemas import Unit, UnitIn
from .authentication import security
from ..utils import update
from .. import models


router = APIRouter(prefix="/units", tags=["Units"])


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=Unit)
def update_unit(
    id: int,
    unit: UnitIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    return update(id, unit, credentials, db, models.Unit, "Unit")
