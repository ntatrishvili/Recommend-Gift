import requests
#from app.config import settings uncomment this line when you integrate this file in the project

def search_amazon(query, category, price):
    url = f"https://real-time-amazon-data.p.rapidapi.com/search"
    
    min_price = price * 0.8
    max_price = price * 1.2
    
    querystring = {
        "query": query,
        # "category": category,
        "min_price": min_price,
        "max_price": max_price,
        "country": "US"
    }
    
    headers = {
        "X-RapidAPI-Key": "c5faa0505cmsh791dce67e35abdap1b8b3djsn3611a3dd3863", #settings.amazon_api_key should be used when you intagrate this file in the project
        "X-RapidAPI-Host": "real-time-amazon-data.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        data = response.json()
        products = data["data"]["products"]
        sorted_products = sorted(products, key=lambda x: x["product_star_rating"], reverse=True)
        top_3_products = sorted_products[:3]
        return top_3_products
    else:
        return {"error": "Failed to retrieve data"}

# Example usage
results = search_amazon("tennis racket", "Sports & Outdoors", 50)
print(results)
