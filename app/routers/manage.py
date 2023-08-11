from fastapi import Depends, status, APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..schemas import ManageData
from .authentication import security
from datetime import date
from ..utils import decode_token


router = APIRouter(prefix="/manage", tags=["Manage"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=ManageData)
def get_manage_data(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    workouts = db.query(models.Workout).filter(models.Workout.user_id == user_id).all()
    programs = db.query(models.Program).filter(models.Program.user_id == user_id).all()
    progressions = (
        db.query(models.Progression).filter(models.Progression.user_id == user_id).all()
    )
    unit = db.query(models.Unit).filter(models.Unit.user_id == user_id).first()
    return {
        "workouts": workouts,
        "programs": programs,
        "progressions": progressions,
        "unit": unit,
    }
