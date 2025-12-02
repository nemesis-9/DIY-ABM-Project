from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from bson import ObjectId


class InventorySchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    agent: PyObjectId = Field(default_factory=PyObjectId, alias='agent')
    items: dict = {}
    pos: dict = {}
    isActive: bool = True

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        orm_mode = True
        