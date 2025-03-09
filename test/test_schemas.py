import pytest
from pydantic import ValidationError
from app.schemas import GiftRecommendation


def test_gift_recommendation_required_fields():
    data = {
        "name": "Tennis Racket",
        "price": 150.00,
        "category": "sport",
        "reason": "Suitable for tennis enthusiasts"
    }
    recommendation = GiftRecommendation(**data)
    assert recommendation.name == "Tennis Racket"
    assert recommendation.price == 150.00
    assert recommendation.category == "sport"
    assert recommendation.reason == "Suitable for tennis enthusiasts"


def test_gift_recommendation_optional_fields():
    data = {
        "name": "Tennis Racket",
        "price": 150.00,
        "category": "sport",
        "reason": "Suitable for tennis enthusiasts",
        "url": "http://example.com/tennis-racket",
        "image": "http://example.com/tennis-racket.jpg"
    }
    recommendation = GiftRecommendation(**data)
    assert recommendation.url == "http://example.com/tennis-racket"
    assert recommendation.image == "http://example.com/tennis-racket.jpg"


def test_gift_recommendation_missing_required_fields():
    data = {
        "price": 150.00,
        "category": "sport",
        "reason": "Suitable for tennis enthusiasts"
    }
    with pytest.raises(ValidationError):
        GiftRecommendation(**data)


def test_gift_recommendation_invalid_price():
    data = {
        "name": "Tennis Racket",
        "price": "invalid_price",
        "category": "sport",
        "reason": "Suitable for tennis enthusiasts"
    }
    with pytest.raises(ValidationError):
        GiftRecommendation(**data)
