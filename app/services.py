import logging
from typing import List
from openai import AsyncOpenAI
from app.config import settings
from app.schemas import GiftRecommendation

logger = logging.getLogger(__name__)

class GiftRecommender:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.gpt_model = settings.gpt_model

    async def generate_recommendations(self, request) -> List[GiftRecommendation]:
        """Main recommendation workflow"""
        try:
            # Step 1: Analyze interests with GPT
            analysis = await self._analyze_interests(request.interests)
            
            # Step 2: Generate gift ideas
            raw_recommendations = await self._get_gpt_recommendations(
                analysis, request.budget, request.occasion
            )
            
            return self._process_recommendations(raw_recommendations)

        except Exception as e:
            logger.error(f"Recommendation failed: {str(e)}")
            raise

    async def _analyze_interests(self, interests: str) -> dict:
        """Use GPT for interest analysis"""
        response = await self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{
                "role": "user",
                "content": f"""Analyze these interests for gift recommendations: {interests}
                Return JSON with: primary_category, key_keywords, sentiment_analysis"""
            }],
            temperature=0.7
        )
        return eval(response.choices[0].message.content)

    async def _get_gpt_recommendations(self, analysis: dict, budget: float, occasion: str) -> list:
        """Get gift ideas from GPT"""
        response = await self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{
                "role": "user",
                "content": f"""Generate 5 gift recommendations matching:
                - Category: {analysis['primary_category']}
                - Budget: ${budget}
                - Occasion: {occasion}
                Return JSON list with item_name, price_estimate, category, reason, confidence_score"""
            }],
            temperature=0.5
        )
        return eval(response.choices[0].message.content)

    def _process_recommendations(self, raw_data: list) -> List[GiftRecommendation]:
        """Convert raw data to validated recommendations"""
        return [GiftRecommendation(**item) for item in raw_data]