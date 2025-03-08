# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class GiftRequest(BaseModel):
    interests: str
    occasion: str
    budget: float

class GiftRecommendation(BaseModel):
    name: str
    price: float
    category: str
    reason: str
    url: Optional[str] = None
    image: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[GiftRecommendation]
    search_id: str