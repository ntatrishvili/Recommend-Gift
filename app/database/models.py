from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.sql import func
from app.database.session import Base


class GiftSearchLog(Base):
    __tablename__ = "gift_searches"

    id = Column(String, primary_key=True, index=True)
    search_params = Column(JSON)
    recommendations = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
