from fastapi import Depends, status, APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from .. import schemas
from ..utils import hash, add_to_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = models.User.get_users(db)
    return users


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = models.User.get_user(db, id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    # user.password = hash(user.password)
    # created_user = models.User(**user.model_dump())
    # add_to_db(created_user, db)
    # created_profile = models.Profile(
    #     username=created_user.username,
    #     email=created_user.email,
    #     user_id=created_user.id,
    # )
    # add_to_db(created_profile, db)
    # created_unit = models.Unit(user_id=created_user.id)
    # add_to_db(created_unit, db)
    # return created_user
    user = models.User.create_user(user, db)
    return user
