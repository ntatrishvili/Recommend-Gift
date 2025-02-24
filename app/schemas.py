from pydantic import BaseModel
from typing import List

class GiftRequest(BaseModel):
    interests: str
    budget: float
    occasion: str

class GiftRecommendation(BaseModel):
    name: str
    price: float
    category: str
    reason: str

class RecommendationResponse(BaseModel):
    recommendations: List[GiftRecommendation]
    search_id: str