# Gift Recommendation API 🎁

A smart gift recommendation engine that uses OpenAI's AI capabilities combined with Amazon's product catalog to suggest perfect gifts based on personalized criteria.

## Features ✨

- **AI-Powered Recommendations**: Uses OpenAI to understand nuanced preferences and suggest thoughtful gifts
- **Amazon Integration**: Recommends real, purchasable products from Amazon
- **Personalized Criteria**: Considers:
  - Relationship to recipient (partner, friend, colleague, etc.)
  - Budget range
  - Recipient's interests and preferences
  - Occasion (birthday, anniversary, holiday, etc.)
- **Simple API Interface**: Easy-to-use endpoints for integration with your applications

## How It Works ⚙️

1. User provides details about:
   - Who they're shopping for
   - Their relationship
   - Budget
   - Interests/preferences
   - Occasion
2. The system uses OpenAI to analyze these inputs and generate gift ideas
3. The Amazon API is queried for real products matching these ideas
4. Curated recommendations are returned to the user

## Installation & Setup 🛠️

### Prerequisites
- Python 3.8+
- OpenAI API key
- Amazon Product Advertising API credentials
- FastAPI (included in requirements.txt)

### Steps
1. Clone the repository:
```bash
git clone https://github.com/ntatrishvili/Recommend-Gift.git
cd Recommend-Gift
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_openai_key_here
AMAZON_API_KEY=your_amazon_key_here
AMAZON_API_SECRET=your_amazon_secret_here
AMAZON_ASSOCIATE_TAG=your_associate_tag
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints 🌐

### Get Gift Recommendations
`POST /recommendations`

**Request Body:**
```json
{
  "relationship": "friend",
  "occasion": "birthday",
  "interests": ["technology", "gaming"],
  "budget": {
    "min": 50,
    "max": 100
  },
  "recipient_age": 28,
  "recipient_gender": "male"
}
```

**Successful Response:**
```json
{
  "recommendations": [
    {
      "name": "Wireless Gaming Mouse",
      "description": "High-performance wireless mouse with customizable buttons",
      "price": 79.99,
      "amazon_url": "https://www.amazon.com/...",
      "reason": "Matches their interest in gaming and fits within your budget"
    },
    {
      "name": "Smart Watch",
      "description": "Feature-rich smartwatch with fitness tracking",
      "price": 89.99,
      "amazon_url": "https://www.amazon.com/...",
      "reason": "Great tech gadget for a 28-year-old with interest in technology"
    }
  ]
}
```

## Example Usage 🚀

```python
import requests

url = "http://localhost:8000/recommendations"
data = {
    "relationship": "mother",
    "occasion": "mother's day",
    "interests": ["gardening", "reading"],
    "budget": {"min": 30, "max": 80},
    "recipient_age": 55,
    "recipient_gender": "female"
}

response = requests.post(url, json=data)
print(response.json())
```

## Contributing 🤝
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## Contact 📧
Nia Tatrishvili - nia.tatrishvili@gmail.com

Luka Matchavariani - lukamatchavariani60@gmail.com
