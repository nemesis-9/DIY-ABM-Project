from pydantic import BaseModel, Field
from .PyObjectId import PyObjectId
from bson import ObjectId
from typing import Dict, Any, Union


class FoodItemDetails(BaseModel):
    count: int = Field(..., description='Number of items')
    cal: int = Field(..., description='Calorie value per item')


class DrinkItemDetails(BaseModel):
    count: int = Field(..., description='Number of items')
    litres: int = Field(..., description='Litres value per item')
    cal: int = Field(..., description='Calorie value per item')


class InventorySchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    agent: PyObjectId = Field(default_factory=PyObjectId, alias='agent')
    foods: Dict[str, FoodItemDetails] = Field(default_factory=dict)
    drinks: Dict[str, DrinkItemDetails] = Field(default_factory=dict)
    pos: dict = Field(default_factory=dict)
    isActive: bool = True

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        orm_mode = True
        