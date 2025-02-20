# app/services.py
import random
from typing import List
from .schemas import GiftRecommendation

def generate_gift_categories(age: int, hobbies: List[str], favorite_tv_shows: List[str], budget: float, relationship: str, additional_preferences: str) -> List[str]:
    """
    Mock function to generate gift categories based on user input.
    """
    prompt = (
        f"Given the following user preferences, suggest relevant gift categories. "
        f"The categories should be among the following options: Tech Gadgets, Books, Fashion Accessories, Camera Accessories, Travel Gear, Home Decor, Eco-Friendly Products.\n\n"
        f"Age: {age}\n"
        f"Hobbies: {', '.join(hobbies)}\n"
        f"Favorite TV Shows: {', '.join(favorite_tv_shows)}\n"
        f"Budget: ${budget}\n"
        f"Relationship: {relationship}\n"
        f"Additional Preferences: {additional_preferences}\n\n"
        f"Categories:"
    )

    categories = []
    
    if age < 18:
        categories.append("Toys")
    elif 18 <= age < 30:
        categories.extend(["Tech Gadgets", "Books", "Fashion Accessories"])
    else:
        categories.extend(["Home Decor", "Kitchen Appliances", "Books"])
    
    if "photography" in hobbies:
        categories.append("Camera Accessories")
    if "traveling" in hobbies:
        categories.append("Travel Gear")
    
    if "eco-friendly" in additional_preferences.lower():
        categories.append("Sustainable Products")
    
    # Remove duplicates
    categories = list(set(categories))
    
    return categories

def fetch_gift_suggestions(categories: List[str], budget: float) -> List[GiftRecommendation]:
    """
    Mock function to fetch gift suggestions based on categories and budget.
    """
    mock_products = {
        "Tech Gadgets": [
            {
                "product_name": "Wireless Earbuds",
                "price": 99.99,
                "product_link": "https://amazon.com/dp/B08XYZ1234",
                "image_url": "https://amazon.com/images/B08XYZ1234.jpg",
                "description": "High-quality wireless earbuds with noise cancellation."
            },
            {
                "product_name": "Smartwatch",
                "price": 199.99,
                "product_link": "https://amazon.com/dp/B07XYZ5678",
                "image_url": "https://amazon.com/images/B07XYZ5678.jpg",
                "description": "Stylish smartwatch with multiple health tracking features."
            }
        ],
        "Books": [
            {
                "product_name": "Bestselling Novel",
                "price": 15.99,
                "product_link": "https://amazon.com/dp/B08XYZ9101",
                "image_url": "https://amazon.com/images/B08XYZ9101.jpg",
                "description": "An engaging novel that captivates readers from start to finish."
            }
        ],
        "Sustainable Products": [
            {
                "product_name": "Reusable Water Bottle",
                "price": 25.00,
                "product_link": "https://amazon.com/dp/B08XYZ1122",
                "image_url": "https://amazon.com/images/B08XYZ1122.jpg",
                "description": "Eco-friendly reusable water bottle made from sustainable materials."
            }
        ],
        # Add more categories and products as needed
    }
    
    recommendations = []
    
    for category in categories:
        products = mock_products.get(category, [])
        for product in products:
            if product["price"] <= budget:
                recommendations.append(GiftRecommendation(**product))
    
    # Randomly select up to 5 recommendations
    recommendations = random.sample(recommendations, min(len(recommendations), 5))
    
    return recommendations
