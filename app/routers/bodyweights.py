from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from .authentication import security
from ..schemas import BodyWeight, BodyWeightIn
from ..utils import create
from .. import models
from datetime import date


router = APIRouter(prefix="/bodyweights", tags=["Body weights"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=BodyWeight)
def create_bodyweight(
    bodyweight: BodyWeightIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    current_date = {"date": date.today()}
    return create(credentials, db, models.BodyWeight, bodyweight, current_date)
