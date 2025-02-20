import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import get_db, Base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

@pytest.fixture(scope="module")
async def test_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    AsyncTestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession
    )
    
    yield AsyncTestingSessionLocal()
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_recommendation_flow(test_db):
    client = TestClient(app)
    app.dependency_overrides[get_db] = lambda: test_db
    
    # Test valid request
    response = client.post(
        "/recommend",
        json={
            "interests": "tech gadgets",
            "budget": 200.0,
            "occasion": "birthday"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) == 5
    assert "search_summary" in data