from pydantic import BaseModel
from .workouts_schemas import WorkoutSchema
from .programs_schemas import ProgramSchema
from .progressions_schemas import ProgressionSchema
from .units_schemas import UnitSchema


class ManageDataSchema(BaseModel):
    todays_workout: WorkoutSchema | None
    programs: list[ProgramSchema]
    progressions: list[ProgressionSchema]
    unit: UnitSchema
