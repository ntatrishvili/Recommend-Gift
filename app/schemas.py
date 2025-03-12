from pydantic import BaseModel, Field
from typing import List, Optional


class GiftRequest(BaseModel):
    age: int = Field(..., json_schema_extra={"example": 25})
    interests: List[str] = Field(
        ..., json_schema_extra={"example": ["sport", "tennis"]}
    )
    budget: float = Field(..., json_schema_extra={"example": 100.00})
    occasion: str = Field(..., json_schema_extra={"example": "birthday"})
    relationship: Optional[str] = Field(
        None, json_schema_extra={"example": "friend"}
    )
    additional_preferences: Optional[str] = Field(
        None,
        json_schema_extra={"example": "Only eco-friendly products, no food items"},
    )


class GiftRecommendation(BaseModel):
    name: str
    price: str
    url: Optional[str] = None
    image: Optional[str] = None


class RecommendationResponse(BaseModel):
    recommendations: List[GiftRecommendation]
    search_id: str
