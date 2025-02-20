from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from .models import GiftSearchLog

async def create_gift_log(db: AsyncSession, log_data: dict):
    new_log = GiftSearchLog(**log_data)
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

async def get_gift_logs(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(GiftSearchLog).offset(skip).limit(limit))
    return result.scalars().all()

async def delete_all_logs(db: AsyncSession):
    await db.execute(delete(GiftSearchLog))
    await db.commit()