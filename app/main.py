from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.database.session import engine, Base
from app.schemas import GiftRequest, RecommendationResponse
from app.services.ai_service import GiftService
from app.database.session import get_db
from app.database.models import GiftSearchLog
from contextlib import asynccontextmanager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_gifts(
    request: GiftRequest, 
    db: AsyncSession = Depends(get_db)
):
    search_id = str(uuid.uuid4())
    service = GiftService()
    
    try:
        # Generate recommendations
        recommendations = await service.generate_recommendations(request)
        
        # Log to database
        log_entry = GiftSearchLog(
            id=search_id,
            search_params=request.model_dump(),
            recommendations=[r.model_dump() for r in recommendations]
        )
        db.add(log_entry)
        await db.commit()
        
        return {
            "recommendations": recommendations,
            "search_id": search_id
        }
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )
