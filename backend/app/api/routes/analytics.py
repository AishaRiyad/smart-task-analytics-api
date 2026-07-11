from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.analytics_service import calculate_task_summary
from app.services.cache_service import get_cache, set_cache

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

CACHE_KEY = "analytics_summary"


@router.get("/summary")
async def get_analytics_summary(
    db: AsyncSession = Depends(get_db),
):
    return await calculate_task_summary(db)


@router.get("/summary-cached")
async def get_cached_analytics_summary(
    db: AsyncSession = Depends(get_db),
):
    cached_summary = await get_cache(CACHE_KEY)

    if cached_summary is not None:
        cached_summary["source"] = "redis_cache"
        return cached_summary

    summary = await calculate_task_summary(db)
    summary["source"] = "database"

    await set_cache(
        CACHE_KEY,
        summary,
        expire_seconds=60,
    )

    return summary