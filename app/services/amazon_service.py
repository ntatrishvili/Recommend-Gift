import requests
from app.config import settings

async def search_amazon(query, budget):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"

    min_price = budget * 0.8

    querystring = {
        "query": query,
        "min_price": min_price,
        "max_price": budget,
        "country": "US"
    }

    headers = {
        "X-RapidAPI-Key": settings.amazon_api_key,
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        # Check if data and products exist to avoid KeyError
        if not data.get("data", {}).get("products"):
            return None, None, None

        products = data["data"]["products"]

        sorted_products = sorted(
            products,
            key=lambda x: float(x.get("product_star_rating")) if x.get("product_star_rating") is not None else 0.0,
            reverse=True
        )

        top_product = sorted_products[0] if sorted_products else None

        if top_product:
            return (
                top_product.get("product_price"),
                top_product.get("product_url"),
                top_product.get("product_photo")
            )
        
    return None, None, None