from .database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship


# -------------------- users --------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(100), nullable=True)
    profile_picture = Column(BYTEA, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


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

    id = Column(Integer, primary_key=True, nullable=False)
    date = Column(String, nullable=False, server_default="now")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User")
    exercises = relationship("WorkoutExercise")


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float(precision=1), nullable=False)
    unit = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    workout_id = Column(
        Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, nullable=False)


# -------------------- programs --------------------
class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=True, server_default="New program")
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
    user = relationship("User")
