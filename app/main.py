from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    units,
    profiles,
    bodyweights,
    workout_exercise_sets,
    manage,
    foods,
)


# base.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Workout site")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# users
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(authentication.router)

# exercises
app.include_router(exercises.router)

# workouts
app.include_router(workouts.router)
app.include_router(workout_exercises.router)
app.include_router(workout_exercise_sets.router)

# programs
app.include_router(programs.router)
app.include_router(program_days.router)
app.include_router(program_exercises.router)

# progressions
app.include_router(progressions.router)
app.include_router(performances.router)

# units
app.include_router(units.router)

# manage
app.include_router(manage.router)

# bodyweights
app.include_router(bodyweights.router)

# foods
app.include_router(foods.router)

# websockets
app.include_router(websockets.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
