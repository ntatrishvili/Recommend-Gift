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
        self.gpt_model = "gpt-3.5-turbo-0125"

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
        prompt = f""""You are an intelligent product selector. Given a list of Amazon products: {products} in JSON format and a user's 
        gift preferences: {preference}, select the single best product that matches the criteria.
        Instructions:
        Analyze the list of products based on the provided criteria, such as price range, brand, rating, Prime eligibility, and other factors given
        in the user's request.
        Choose the product that best matches all or most of the criteria.
        If multiple products are equally suitable, select the one with the highest rating and number of reviews.
        Return the selected product in JSON format with the following keys:
        product_title
        product_price
        product_url
        product_photo
        
        YOUR RESPONSE DOESN'T NEED TO INCLUDE EXPLANATION OR JUSTIFICATION. ONLY WRITE SELECTED PRODUCT IN JSON FORMAT LIKE BELOW:
        {{
            "product_title": "Product 1",
            "product_price": "100.00",
            "product_url": "https://www.amazon.com/product1",
            "product_photo": "https://www.amazon.com/product1.jpg"
        }}"""

        response = await self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        try:
            result = json.loads(response.choices[0].message.content)
            return result
        except (json.JSONDecodeError, AttributeError, IndexError) as e:
            logger.error(f"Failed to parse OpenAI response: {str(e)}")
            return {} 