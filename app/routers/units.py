from fastapi import APIRouter, Depends, Security, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from ..schemas import Unit, UnitIn
from .authentication import security
from ..utils import update, get_item
from .. import models


router = APIRouter(prefix="/units", tags=["Units"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=Unit)
def get_unit(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    unit = db.query(models.Unit).filter(models.Unit.user_id == user_id).first()
    return unit


@router.put("/", status_code=status.HTTP_200_OK, response_model=Unit)
def update_unit(
    unit: UnitIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    query = db.query(models.Unit).filter(models.Unit.user_id == user_id)
    query.update(unit.model_dump())
    db.commit()
    return query.first()
