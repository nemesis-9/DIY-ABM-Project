from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from bson import ObjectId


class SchemaAgent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    name: str
    age: int
    pos: dict = {}
    state: str
    hunger: int
    hunger_max: int
    metabolism: int
    hp: int
    skills: dict = {}
    inventory: dict = {}

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
        orm_mode = True
