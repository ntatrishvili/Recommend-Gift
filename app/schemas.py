from pydantic import BaseModel
from typing import List, Optional

class GiftRequest(BaseModel):
    interests: str
    budget: float
    occasion: str
    recipient_age: Optional[int] = None

class GiftRecommendation(BaseModel):
    item_name: str
    price_estimate: float
    category: str
    reason: str
    confidence_score: float

class RecommendationResponse(BaseModel):
    recommendations: List[GiftRecommendation]
    search_summary: str