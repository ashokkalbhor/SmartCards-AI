from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.core.database import get_async_db
from app.core.security import get_current_user
from app.models.analytics import AnalyticsEvent
from app.models.user import User
from datetime import datetime, timedelta, timezone
from typing import Optional

router = APIRouter()

# Helper: normalize path to root-level

def normalize_path_root(path: str) -> str:
    if not path or path == '/':
        return '/'
    segs = [s for s in path.split('/') if s]
    return '/' + segs[0] if segs else '/'

# POST /analytics: ingest event (only for logged-in users)
@router.post("/analytics", status_code=201)
async def ingest_analytics_event(
    event: dict,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    # Only allow logged-in users
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")
    # Validate event
    path = event.get("path")
    duration_seconds = event.get("duration_seconds")
    event_name = event.get("event_name", "page_duration")
    properties = event.get("properties")
    if not path or duration_seconds is None:
        raise HTTPException(status_code=400, detail="Missing path or duration_seconds")
    path_root = normalize_path_root(path)
    db_event = AnalyticsEvent(
        event_name=event_name,
        user_id=current_user.id,
        path_root=path_root,
        duration_seconds=duration_seconds,
        properties=str(properties) if properties else None,
    )
    db.add(db_event)
    await db.commit()
    return {"status": "ok"}

# GET /admin/analytics/dau: daily active users (last 30 days)
@router.get("/admin/analytics/dau")
async def get_dau(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    # Only allow logged-in users
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")
    # Compute DAU for last 30 days
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    start = now - timedelta(days=30)
    stmt = select(
        func.strftime('%Y-%m-%d', AnalyticsEvent.created_at).label('day'),
        func.count(func.distinct(AnalyticsEvent.user_id)).label('dau')
    ).where(
        AnalyticsEvent.created_at >= start
    ).group_by('day').order_by('day')
    result = await db.execute(stmt)
    data = [{"day": row.day, "dau": row.dau} for row in result]
    return data

# GET /admin/analytics/mau: monthly active users (last 30 days)
@router.get("/admin/analytics/mau")
async def get_mau(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    start = now - timedelta(days=30)
    stmt = select(func.count(func.distinct(AnalyticsEvent.user_id)).label('mau')).where(
        AnalyticsEvent.created_at >= start
    )
    result = await db.execute(stmt)
    mau = result.scalar() or 0
    return {"mau": mau}

# GET /admin/analytics/top-pages: top pages by views (last 30 days)
@router.get("/admin/analytics/top-pages")
async def get_top_pages(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    start = now - timedelta(days=30)
    stmt = select(
        AnalyticsEvent.path_root,
        func.count().label('views')
    ).where(
        AnalyticsEvent.created_at >= start
    ).group_by(AnalyticsEvent.path_root).order_by(func.count().desc()).limit(20)
    result = await db.execute(stmt)
    data = [{"path_root": row.path_root, "views": row.views} for row in result]
    return data

# GET /admin/analytics/avg-duration: average time on page (last 30 days)
@router.get("/admin/analytics/avg-duration")
async def get_avg_duration(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Authentication required")
    now = datetime.utcnow().replace(tzinfo=timezone.utc)
    start = now - timedelta(days=30)
    stmt = select(
        AnalyticsEvent.path_root,
        func.avg(AnalyticsEvent.duration_seconds).label('avg_duration')
    ).where(
        AnalyticsEvent.created_at >= start
    ).group_by(AnalyticsEvent.path_root).order_by(func.avg(AnalyticsEvent.duration_seconds).desc()).limit(20)
    result = await db.execute(stmt)
    data = [{"path_root": row.path_root, "avg_duration": row.avg_duration} for row in result]
    return data
