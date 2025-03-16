from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.database.session import engine, Base
from app.schemas import GiftRequest, AmazonGiftRequest, RecommendationResponse, RecommendationUsingAIResponse, RecommendationUsingAmazonResponse, GiftRecommendation
from app.services.ai_service import GiftService
from app.services.amazon_service import search_amazon, search_amazon_only, basic_search_amazon
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
async def recommend_gifts(request: GiftRequest, db: AsyncSession = Depends(get_db)):
    search_id = str(uuid.uuid4())
    service = GiftService()

    try:
        # Generate recommendations
        recommendations = await service.generate_recommendations(request)

        for recommendation in recommendations:
            product_price, product_url, product_image = await search_amazon(recommendation.name, request.budget)
            
            recommendation.price = str(product_price) if product_price else "Unknown"
            recommendation.url = str(product_url) if product_url else "No product found"
            recommendation.image = str(product_image) if product_image else "No image available"

        
        # Log to database
        log_entry = GiftSearchLog(
            id=search_id,
            search_params=request.model_dump(),
            recommendations=[r.model_dump() for r in recommendations],
        )
        db.add(log_entry)
        await db.commit()

        return {"recommendations": recommendations, "search_id": search_id}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")
    
@app.post("/recommend-with-double-call", response_model=RecommendationResponse)
async def recommend_gift_with_double_call(request: GiftRequest, db: AsyncSession = Depends(get_db)):
    search_id = str(uuid.uuid4())
    service = GiftService()

    try:
        # Generate recommendations
        recommendations = await service.generate_recommendations(request)
        recommendation_list = [recommendation.name for recommendation in recommendations]
        print(recommendation_list)
        print("________________")
        
        real_recommendations = []
        for recommendation in recommendation_list:
            products = await basic_search_amazon(recommendation, request.budget)

            if products:
                sorted_products = sorted(
                    products,
                    key=lambda x: float(x.get("product_star_rating")) if x.get("product_star_rating") is not None else 0.0,
                    reverse=True
                )
                sorted_products = sorted_products[:25]
                print(sorted_products)
                print("________________")

                if sorted_products:
                    chosen_product = await service.choose_products_based_on_preferences(
                        request.preference, sorted_products
                    )
                    print(chosen_product)
                    print("________________")
                    if chosen_product:
                        real_recommendations.append(
                            GiftRecommendation(
                                name=chosen_product.get("product_title"),
                                price=chosen_product.get("product_price"),
                                url=chosen_product.get("product_url"),
                                image=chosen_product.get("product_photo")
                            )
                        )

        # Log to database
        log_entry = GiftSearchLog(
            id=search_id,
            search_params=request.model_dump(),
            recommendations=[r.model_dump() for r in real_recommendations],
        )
        db.add(log_entry)
        await db.commit()

        return {"recommendations": real_recommendations, "search_id": search_id}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"DoubleCall Recommendation failed: {str(e)}")
    
@app.post("/recommend-using-only-ai", response_model=RecommendationUsingAIResponse)
async def recommend_using_only_ai(request: GiftRequest, db: AsyncSession = Depends(get_db)):
    search_id = str(uuid.uuid4())
    service = GiftService()

    try:
        # Generate recommendations using AI only
        recommendations = await service.generate_recommendations(request)
        recommendation_list = []
        for recommendation in recommendations:
            recommendation_list.append(recommendation.name)
            
        # Log to database
        log_entry = GiftSearchLog(
            id=search_id,
            search_params=request.model_dump(),
            recommendations=[r.model_dump() for r in recommendations],
        )
        db.add(log_entry)
        await db.commit()
        
        return {"recommendations": recommendation_list}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI recommendation failed: {str(e)}")

@app.post("/recommend-using-only-amazon", response_model=RecommendationUsingAmazonResponse)
async def recommend_using_only_amazon(request: AmazonGiftRequest, db: AsyncSession = Depends(get_db)):
    search_id = str(uuid.uuid4())
    
    try:
        recommendations = await search_amazon_only(request.query, request.budget)
        # Log to database
        log_entry = GiftSearchLog(
            id=search_id,
            search_params=request.model_dump(),
            recommendations=[r for r in recommendations],
        )
        db.add(log_entry)
        await db.commit()

        return {"recommendations": recommendations}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Amazon recommendation failed: {str(e)}")