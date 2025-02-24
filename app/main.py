from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "OK", 
        "openai_key": f"{settings.openai_api_key[:3]}... (loaded)"
    }