import logging
import json
from typing import List
from openai import AsyncOpenAI
from app.config import settings
from app.schemas import GiftRecommendation

logger = logging.getLogger(__name__)


class GiftService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("Missing OpenAI API key")

        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.gpt_model = "gpt-4"

    async def generate_recommendations(self, request) -> List[GiftRecommendation]:
        """Generate recommendations using OpenAI"""
        try:
            # Step 1: Get AI suggestions
            ai_products = await self._get_ai_product_names(request)

            # Step 2: Format results
            return self._format_results(ai_products)

        except Exception as e:
            logger.error(f"OpenAI API failed: {str(e)}")
            return await self._get_fallback_ai_recommendations(request)

    async def _get_ai_product_names(self, request) -> List[str]:
        """Get product names from OpenAI"""
        prompt = f"""Generate 5-7 specific product names matching:
        Age: {request.age}
        Interests: {', '.join(request.interests)}
        Occasion: {request.occasion}
        Relationship: {request.relationship or 'N/A'}
        Additional Preferences: {request.additional_preferences or 'N/A'}
        
        Please keep in mind that the budget is ${request.budget} dollars only.

        Return ONLY a JSON array like: ["Product 1", "Product 2"]"""

        response = await self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error("Failed to parse OpenAI response")
            return []

    def _format_results(self, product_names: List[str]) -> List[GiftRecommendation]:
        """Return results in a user-friendly format"""
        recommendations = [
            GiftRecommendation(
                name=name,
                price=0,
                category="General",
                reason="AI-generated suggestion",
                url=None,
                image=None,
            )
            for name in product_names
        ]

        return (recommendations)[:5]

    async def _get_fallback_ai_recommendations(
        self, request
    ) -> List[GiftRecommendation]:
        """Fallback to a draft implementation if requests fail"""
        # ... (keep your existing OpenAI implementation) ...
        # not implemented and not sure if it needs to be
