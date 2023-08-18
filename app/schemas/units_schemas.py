from pydantic import BaseModel


class UnitInSchema(BaseModel):
    unit: str


class UnitSchema(UnitInSchema):
    id: int
    user_id: int
