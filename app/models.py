from datetime import datetime
from typing import Self

from pydantic import EmailStr
from .database import Base
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    text,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from .schemas import UserIn
from .utils import hash, add_to_db


# -------------------- users --------------------


# -------------------- blacklisted tokens --------------------


# -------------------- explore exercises --------------------


# -------------------- workouts --------------------


# -------------------- programs --------------------


# -------------------- progressions --------------------


# -------------------- weight change --------------------
