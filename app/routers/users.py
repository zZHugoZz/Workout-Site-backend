from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from ..utils import hash


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.UserOut]
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.UserOut
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} doesn't exist"
        )
    return user


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut
)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    created_user = models.User(**user.model_dump())
    db.add(created_user)
    db.commit()
    db.refresh(created_user)
    return created_user


