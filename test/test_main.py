import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from unittest.mock import patch, AsyncMock

# FILE: test/test_main.py


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_db():
    return AsyncMock(AsyncSession)


@pytest.fixture
def mock_gift_service():
    with patch("app.services.ai_service.GiftService") as mock:
        yield mock


@pytest.mark.anyio
async def test_recommend_gifts_success(client, mock_db, mock_gift_service):
    mock_gift_service.return_value.generate_recommendations = AsyncMock(
        return_value=[
            {
                "name": "Tennis Racket",
                "price": 150.00,
                "category": "sport",
                "reason": "Suitable for tennis enthusiasts",
            }
        ]
    )

    request_data = {
        "age": 25,
        "interests": ["sport", "tennis"],
        "budget": 100.00,
        "occasion": "birthday",
        "relationship": "friend",
        "additional_preferences": "Only eco-friendly products, no food items",
    }

    response = await client.post("/recommend", json=request_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "recommendations" in response_data
    assert "search_id" in response_data
    assert len(response_data["recommendations"]) == 1
    assert response_data["recommendations"][0]["name"] == "Tennis Racket"


@pytest.mark.anyio
async def test_recommend_gifts_failure(client, mock_db, mock_gift_service):
    mock_gift_service.return_value.generate_recommendations = AsyncMock(
        side_effect=Exception("AI service error")
    )

    request_data = {
        "age": 25,
        "interests": ["sport", "tennis"],
        "budget": 100.00,
        "occasion": "birthday",
        "relationship": "friend",
        "additional_preferences": "Only eco-friendly products, no food items",
    }

    response = await client.post("/recommend", json=request_data)
    assert response.status_code == 500
    response_data = response.json()
    assert response_data["detail"] == "Recommendation failed: AI service error"
