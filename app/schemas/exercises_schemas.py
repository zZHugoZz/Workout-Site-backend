from pydantic import BaseModel


class ExerciseSchema(BaseModel):
    id: int
    name: str
    link: str
