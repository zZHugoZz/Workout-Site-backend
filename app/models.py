from .database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class BlackListedToken(Base):
    __tablename__ = "blacklisted_tokens"

    id = Column(Integer, primary_key=True, nullable=False)
    token = Column(String(300), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    link = Column(String(50), nullable=False)


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, nullable=False)
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


class ProgamDay(Base):
    __tablename__ = "program_days"

    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    program_id = Column(
        Integer, ForeignKey("programs.id", ondelete="CASCADE"), nullable=False
    )
    exercises = relationship("ProgramExercise")


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
