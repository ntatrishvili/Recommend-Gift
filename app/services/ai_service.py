import logging
import json
from typing import List
from openai import AsyncOpenAI
from app.config import settings
from app.schemas import GiftRecommendation
from .amazon_api import AmazonAPI, AmazonAPIError

logger = logging.getLogger(__name__)

class GiftService:
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("Missing OpenAI API key")
        
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.amazon = AmazonAPI()
        self.gpt_model = "gpt-4"

    async def generate_recommendations(self, request) -> List[GiftRecommendation]:
            """Generate recommendations using OpenAI and verify with Amazon"""
            try:
                # Step 1: Get AI suggestions
                ai_products = await self._get_ai_product_names(request)
                
                # Step 2: Search Amazon
                amazon_results = await self._get_amazon_products(ai_products, request.budget)
                
                # Step 3: Format results
                return self._format_results(amazon_results, ai_products)
                
            except AmazonAPIError as e:
                logger.error(f"Amazon API failed: {str(e)}")
                return await self._get_fallback_ai_recommendations(request)
            
    async def _get_ai_product_names(self, request) -> List[str]:
        """Get product names from OpenAI"""
        prompt = f"""Generate 5-7 specific product names matching:
        - Interests: {request.interests}
        - Budget: ${request.budget}
        - Occasion: {request.occasion}
        
        Return ONLY a JSON array like: ["Product 1", "Product 2"]"""
        
        response = await self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.error("Failed to parse OpenAI response")
            return []

    async def _get_amazon_products(self, product_names: List[str], budget: float) -> List[dict]:
        """Search Amazon for products"""
        try:
            return await self.amazon.search_products(
                keywords=" ".join(product_names),
                max_price=budget
            )
        except AmazonAPIError:
            return []
        
    def _format_results(self, amazon_results: List[dict], ai_names: List[str]) -> List[GiftRecommendation]:
        """Combine verified products with AI fallbacks"""
        verified = [
            GiftRecommendation(
                name=product["name"],
                price=product["price"],
                category=product["category"],
                reason=f"Available on Amazon (${product['price']})",
                url=product["url"],
                image=product["image"]
            ) for product in amazon_results
        ]
        
        # Add AI fallbacks for missing products
        ai_fallback = [
            GiftRecommendation(
                name=name,
                price=0,
                category="General",
                reason="AI-generated suggestion",
                url=None,
                image=None
            ) for name in ai_names if not any(p.name == name for p in verified)
        ]
        
        return (verified + ai_fallback)[:5]

    async def _get_fallback_ai_recommendations(self, request) -> List[GiftRecommendation]:
        """Fallback to pure AI suggestions if Amazon fails"""
        # ... (keep your existing OpenAI implementation) ...
        # not implemented and not sure if it needs to be
