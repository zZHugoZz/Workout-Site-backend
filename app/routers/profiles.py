from fastapi import APIRouter, Depends, status, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from ..schemas import Profile
from .authentication import security
from .. import models


router = APIRouter(prefix="/profiles", tags=["Profiles"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=Profile)
def get_profile(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    return profile
