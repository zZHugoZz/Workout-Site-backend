from datetime import datetime
from typing import Self
from fastapi import HTTPException, status
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
from sqlalchemy.orm import Mapped, mapped_column, Session
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship
from .schemas import UserIn
from .utils import hash, add_to_db


# -------------------- users --------------------
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username} email={self.email})"

    @classmethod
    def get_users(cls, session: Session) -> list[Self]:
        query = select(cls)
        users = session.execute(query).scalars()
        return users

    @classmethod
    def get_user(cls, session: Session, id: int) -> Self:
        query = select(cls).where(cls.id == id)
        user = session.execute(query).scalar()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id: {id} doesn't exist",
            )
        return user

    @classmethod
    def create_user(cls, user: UserIn, session: Session) -> Self:
        user.password = hash(user.password)
        created_user = cls(**user.model_dump())
        add_to_db(created_user, session)
        created_profile = Profile(
            username=created_user.username,
            email=created_user.email,
            user_id=created_user.id,
        )
        add_to_db(created_profile, session)
        created_unit = Unit(user_id=created_user.id)
        add_to_db(created_unit, session)
        return created_user


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(100), nullable=True)
    profile_picture = Column(BYTEA, nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user = relationship("User")


# -------------------- blacklisted tokens --------------------
class BlackListedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String(300), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


# -------------------- explore exercises --------------------
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    link = Column(String(50), nullable=False)


# -------------------- workouts --------------------
class Workout(Base):
    __tablename__ = "workouts"

    # id = Column(Integer, primary_key=True, nullable=False)
    # date = Column(String, nullable=False, server_default="now")
    # created_at = Column(
    #     TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    # )
    # user_id = Column(
    #     Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    # )
    # user = relationship("User")
    # exercises = relationship("WorkoutExercise")
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    date: Mapped[str] = mapped_column(
        String(50), nullable=False, server_default="today"
    )
    created_at = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped[User] = relationship()

    def __repr__(self) -> str:
        return f"Workout(id={self.id}, date={self.date})"


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    n_sets = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    workout_id = Column(
        Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, nullable=False)
    sets = relationship("WorkoutExerciseSet")


class WorkoutExerciseSet(Base):
    __tablename__ = "workout_exercise_sets"

    id = Column(Integer, primary_key=True, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float(precision=1), nullable=False)
    workout_exercise_id = Column(
        Integer, ForeignKey("workout_exercises.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(Integer, nullable=False)


# -------------------- programs --------------------
class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False, server_default="New program")
    description = Column(String(300), nullable=False, server_default="No description")
    n_days = Column(Integer, nullable=False, server_default="7")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User")
    days = relationship("ProgramDay")


class ProgramDay(Base):
    __tablename__ = "program_days"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    program_id = Column(
        Integer, ForeignKey("programs.id", ondelete="CASCADE"), nullable=False
    )
    exercises = relationship("ProgramExercise")
    user_id = Column(Integer, nullable=False)


class ProgramExercise(Base):
    __tablename__ = "program_exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    min_sets = Column(Integer, nullable=False)
    max_sets = Column(Integer, nullable=False)
    min_reps = Column(Integer, nullable=False)
    max_reps = Column(Integer, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    day_id = Column(
        Integer, ForeignKey("program_days.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, nullable=False)


# -------------------- progressions --------------------
class Progression(Base):
    __tablename__ = "progressions"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    color = Column(String(100), nullable=False, server_default="#FF7543")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User")
    performances = relationship("Performance")


class Performance(Base):
    __tablename__ = "performances"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(String(100), nullable=False, server_default="today")
    weight = Column(Float(precision=1), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    progression_id = Column(
        Integer, ForeignKey("progressions.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, nullable=False)


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, nullable=False)
    unit = Column(String(100), nullable=False, server_default="Kg")
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )


# -------------------- weight change --------------------
class BodyWeight(Base):
    __tablename__ = "body_weights"

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(String(100), nullable=False, server_default="today")
    weight = Column(Float(precision=1), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class BodyWeightUnit(Base):
    __tablename__ = "body_weight_units"

    id = Column(Integer, primary_key=True, nullable=False)
    unit = Column(String(100), nullable=False, server_default="Kg")
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
