# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_suggest_gifts_success():
    payload = {
        "age": 25,
        "hobbies": ["photography", "traveling"],
        "favorite_tv_shows": ["Stranger Things", "The Crown"],
        "budget": 100.00,
        "relationship": "friend",
        "additional_preferences": "eco-friendly products"
    }
    
    response = client.post("/suggest-gifts", json=payload)
    assert response.status_code == 200
    assert "recommendations" in response.json()
    assert len(response.json()["recommendations"]) > 0

def test_suggest_gifts_no_recommendations():
    payload = {
        "age": 5,
        "hobbies": ["unknown hobby"],
        "favorite_tv_shows": ["unknown show"],
        "budget": 5.00,
        "relationship": "family",
        "additional_preferences": "unknown preference"
    }
    
    response = client.post("/suggest-gifts", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "No gift recommendations found for the given criteria."

def test_suggest_gifts_invalid_input():
    payload = {
        "age": "twenty-five",  # Invalid age type
        "hobbies": ["photography"],
        "favorite_tv_shows": ["Stranger Things"],
        "budget": 100.00
    }
    
    response = client.post("/suggest-gifts", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
