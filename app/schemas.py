# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel, Field

class GiftRequest(BaseModel):
    age: int = Field(
        ..., 
        json_schema_extra={"example": 25}
    )
    hobbies: List[str] = Field(
        ..., 
        json_schema_extra={"example": ["photography", "traveling"]}
    )
    favorite_tv_shows: List[str] = Field(
        ..., 
        json_schema_extra={"example": ["Stranger Things", "The Crown"]}
    )
    budget: float = Field(
        ..., 
        json_schema_extra={"example": 100.00}
    )
    relationship: Optional[str] = Field(
        None, 
        json_schema_extra={"example": "friend"}
    )
    additional_preferences: Optional[str] = Field(
        None, 
        json_schema_extra={"example": "eco-friendly products"}
    )

class GiftRecommendation(BaseModel):
    product_name: str
    price: float
    product_link: str
    image_url: str
    description: str

class GiftResponse(BaseModel):
    recommendations: List[GiftRecommendation]
