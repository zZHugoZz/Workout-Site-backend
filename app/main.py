from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import (
    users,
    exercises,
    authentication,
    workouts,
    workout_exercises,
    websockets,
    programs,
    program_days,
    program_exercises,
    progressions,
    performances,
)


# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(exercises.router)
app.include_router(authentication.router)
app.include_router(workouts.router)
app.include_router(workout_exercises.router)
app.include_router(programs.router)
app.include_router(program_days.router)
app.include_router(program_exercises.router)
app.include_router(progressions.router)
app.include_router(performances.router)
app.include_router(websockets.router)
