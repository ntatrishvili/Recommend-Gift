import logging
import json
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

    async def generate_recommendations(self, request):
        """Core recommendation logic with improved JSON handling"""
        try:
            prompt = f"""
            Suggest 5 gift ideas matching:
            - Interests: {request.interests}
            - Budget: ${request.budget}
            - Occasion: {request.occasion}

            **Return ONLY a JSON list (without extra text) in the following format:**
            [
                {{
                    "name": "Item name",
                    "price": 99.99,  # Number without quotes or $
                    "category": "Category",
                    "reason": "Explanation"
                }}
            ]
            """

            response = await self.client.chat.completions.create(
                model=self.gpt_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            raw_content = response.choices[0].message.content.strip()

            # Attempt to parse JSON safely
            try:
                raw_data = json.loads(raw_content)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON from OpenAI: {raw_content}")
                raise ValueError("Invalid response format from OpenAI") from e

            return self._process_recommendations(raw_data)

        except Exception as e:
            logger.error(f"Recommendation failed: {str(e)}")
            raise

    def _process_recommendations(self, raw_data: list):
        """Cleans and validates the OpenAI response"""
        processed = []
        for item in raw_data:
            try:
                # Ensure 'price' is a float and remove unnecessary characters
                item["price"] = float(str(item["price"]).replace("$", "").strip())
                
                # Validate the final schema
                processed.append(GiftRecommendation(**item))
            except (ValueError, KeyError, TypeError) as e:
                logger.error(f"Invalid item format: {item} - Error: {e}")
                continue  # Skip bad data instead of crashing
        return processed
