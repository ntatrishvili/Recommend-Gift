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
                price="Unknown",
                url=None,
                image=None,
            )
            for name in product_names
        ]

        return (recommendations)[:5]

    async def choose_products_based_on_preferences(self, preference, products) -> dict:
        """Get product names from OpenAI"""
        prompt = f"""Choose the best option based on the following preferences: {preference}
        from the following list: {products}.

        Return ONLY a JSON OBJECT of the chosen product (no arrays)."""

        response = await self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        try:
            result = json.loads(response.choices[0].message.content)
            # Handle case where response is a list
            if isinstance(result, list):
                return result[0] if result else {}
            return result
        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            logger.error(f"Failed to parse OpenAI response: {str(e)}")
            return {}  # Return empty dict instead of list   