# app/main.py
from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import GiftRequest, GiftResponse, GiftRecommendation
from .services import generate_gift_categories, fetch_gift_suggestions
from .logger import logger

app = FastAPI(
    title="GiftAI POC",
    description="An API to suggest gifts based on user preferences.",
    version="1.0.0"
)

@app.post("/suggest-gifts", response_model=GiftResponse)
def suggest_gifts(gift_request: GiftRequest):
    logger.info(f"Received gift request: {gift_request}")

    try:
        # Generate gift categories based on user input
        
        categories = generate_gift_categories(
            age=gift_request.age,
            hobbies=gift_request.hobbies,
            favorite_tv_shows=gift_request.favorite_tv_shows,
            budget=gift_request.budget,
            relationship=gift_request.relationship or "friend",
            additional_preferences=gift_request.additional_preferences or ""
        )
        logger.info(f"Generated categories: {categories}")

        # Fetch gift suggestions based on categories and budget
        recommendations = fetch_gift_suggestions(categories, gift_request.budget)
        logger.info(f"Fetched {len(recommendations)} recommendations.")

        if not recommendations:
            raise HTTPException(status_code=404, detail="No gift recommendations found for the given criteria.")

        return GiftResponse(recommendations=recommendations)

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions without modification
        logger.error(f"HTTPException occurred: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        # Handle unexpected exceptions
        logger.error(f"Error processing gift request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
