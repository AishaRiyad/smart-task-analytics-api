from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.database import get_db
from app.db.models import User
from app.schemas.analytics import AnalyticsDashboardResponse
from app.services.analytics_service import calculate_task_summary
from app.services.cache_service import get_cache, set_cache
from app.services.dashboard_service import get_dashboard_data

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

CACHE_KEY = "analytics_summary"


@router.get("/summary")
def get_analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return calculate_task_summary(
        db=db,
        user_id=current_user.id,
    )


@router.get("/summary-cached")
def get_cached_analytics_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    cache_key = f"{CACHE_KEY}:{current_user.id}"

    cached_summary = get_cache(cache_key)

    if cached_summary:
        cached_summary["source"] = "redis_cache"
        return cached_summary

    summary = calculate_task_summary(
        db=db,
        user_id=current_user.id,
    )
    summary["source"] = "database"

    set_cache(
        cache_key,
        summary,
        expire_seconds=60,
    )

    return summary


@router.get(
    "/dashboard",
    response_model=AnalyticsDashboardResponse,
)
def get_analytics_dashboard(
    days: int = Query(default=7, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_data(
        db=db,
        user_id=current_user.id,
        days=days,
    )