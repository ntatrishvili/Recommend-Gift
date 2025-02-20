from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import GiftRequest, RecommendationResponse
from app.services import GiftRecommender
from app.database.session import get_db, Base
from app.database.models import GiftSearchLog
from app.logger import logger

app = FastAPI(title="GiftsAI", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with get_db() as session:
        await session.begin()
        try:
            await session.run_sync(Base.metadata.create_all)
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database initialization failed: {str(e)}")

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend_gifts(
    request: GiftRequest, 
    db: AsyncSession = Depends(get_db)
):
    start_time = time.time()
    recommender = GiftRecommender()
    
    try:
        recommendations = await recommender.generate_recommendations(request)
        
        log_entry = GiftSearchLog(
            search_params=request.model_dump(),
            recommendations=[r.model_dump() for r in recommendations],
            processing_time=time.time() - start_time,
            model_version=recommender.gpt_model
        )
        
        db.add(log_entry)
        await db.commit()
        
        return {
            "recommendations": recommendations,
            "search_summary": f"Generated {len(recommendations)} recommendations"
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Recommendation service error")