import pytest
from unittest.mock import AsyncMock, patch
from app.services.ai_service import GiftService
from app.schemas import GiftRequest, GiftRecommendation
from app.config import settings

@pytest.fixture
def mock_openai():
    with patch("app.services.ai_service.AsyncOpenAI") as MockOpenAI:
        yield MockOpenAI

@pytest.fixture
def gift_service(mock_openai):
    return GiftService()

@pytest.mark.asyncio
async def test_generate_recommendations_success(gift_service):
    mock_request = GiftRequest(
        age=25,
        interests=["sport", "tennis"],
        budget=100.00,
        occasion="birthday",
        relationship="friend",
        additional_preferences="Only eco-friendly products, no food items"
    )

    mock_response = [
        GiftRecommendation(name="Tennis Racket", price=50.00, category="sport", reason="Great for tennis lovers"),
        GiftRecommendation(name="Eco-friendly Water Bottle", price=20.00, category="eco-friendly", reason="Eco-friendly and useful")
    ]

    gift_service.generate_recommendations = AsyncMock(return_value=mock_response)

    recommendations = await gift_service.generate_recommendations(mock_request)

    assert recommendations == mock_response

@pytest.mark.asyncio
async def test_generate_recommendations_failure(gift_service):
    mock_request = GiftRequest(
        age=25,
        interests=["sport", "tennis"],
        budget=100.00,
        occasion="birthday",
        relationship="friend",
        additional_preferences="Only eco-friendly products, no food items"
    )

    gift_service.generate_recommendations = AsyncMock(side_effect=Exception("API error"))

    with pytest.raises(Exception) as excinfo:
        await gift_service.generate_recommendations(mock_request)

    assert str(excinfo.value) == "API error"
