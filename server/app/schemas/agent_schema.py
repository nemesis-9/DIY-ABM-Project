from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from bson import ObjectId
from typing import Literal


class AgentSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str
    age: int
    gender: Literal['m', 'f', 'M', 'F']

    pos: dict = Field(default_factory=dict)
    state: str

    weight: float
    height: float

    bmr: float
    metabolism: float
    energy_stored: float
    body_hydrate: float
    hungry: float
    thirsty: float
    max_hungry: float
    max_thirsty: float

    hp: int
    skills: dict = Field(default_factory=dict)

    inventory: dict = Field(default_factory=dict)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        orm_mode = True
