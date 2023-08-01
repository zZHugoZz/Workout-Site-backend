from fastapi import APIRouter, Depends, Security, status, security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import decode_token
from ..schemas import ProgresionIn, Progression
from .. import models
from .authentication import security


router = APIRouter(prefix="/progressions", tags=["Progressions"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Progression)
def create_progression(
    progression: ProgresionIn,
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    user_id = decode_token(credentials.credentials)
    created_progression = models.Progression(
        **progression.model_dump(), user_id=user_id
    )
    db.add(created_progression)
    db.commit()
    db.refresh(created_progression)
    return created_progression
