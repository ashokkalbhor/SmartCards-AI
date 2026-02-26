
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analytics import AnalyticsEvent

# Test unauthenticated access
def test_unauthenticated_post_rejected(client):
    resp = client.post("/api/v1/analytics", json={"path": "/cards", "duration_seconds": 10})
    assert resp.status_code == 403

# Test authenticated event submission
@pytest.mark.asyncio
async def test_authenticated_post_inserts_row(client, test_user, auth_headers, async_db: AsyncSession):
    # Post event
    resp = client.post(
        "/api/v1/analytics",
        json={"path": "/cards/123", "duration_seconds": 15},
        headers=auth_headers
    )
    assert resp.status_code == 201

    # Verify database entry using async session
    from sqlalchemy import select
    stmt = select(AnalyticsEvent).filter_by(
        user_id=test_user.id,
        path_root="/cards",
        duration_seconds=15
    )
    result = await async_db.execute(stmt)
    events = result.scalars().all()
    assert len(events) > 0
    
    # Verify event data
    event = events[0]
    assert event.event_name == "page_duration"  # default event name
    assert event.user_id == test_user.id
    assert event.path_root == "/cards"
    assert event.duration_seconds == 15
    assert event.created_at is not None

# Test analytics endpoints
def test_dau_and_mau_endpoints(client, test_user, auth_headers):
    # Insert test events
    for i in range(3):
        resp = client.post(
            "/api/v1/analytics",
            json={"path": f"/cards/{i}", "duration_seconds": 10 + i},
            headers=auth_headers
        )
        assert resp.status_code == 201

    # Test DAU endpoint
    resp = client.get("/api/v1/admin/analytics/dau", headers=auth_headers)
    assert resp.status_code == 200
    dau_data = resp.json()
    assert isinstance(dau_data, list)
    assert len(dau_data) > 0
    assert all(isinstance(day_data, dict) for day_data in dau_data)
    assert all("day" in day_data and "dau" in day_data for day_data in dau_data)
    
    # Test MAU endpoint
    resp = client.get("/api/v1/admin/analytics/mau", headers=auth_headers)
    assert resp.status_code == 200
    mau_data = resp.json()
    assert "mau" in mau_data
    assert isinstance(mau_data["mau"], int)
    assert mau_data["mau"] >= 1  # at least one user (test_user)
    
    # Test Top Pages endpoint
    resp = client.get("/api/v1/admin/analytics/top-pages", headers=auth_headers)
    assert resp.status_code == 200
    pages_data = resp.json()
    assert isinstance(pages_data, list)
    assert len(pages_data) > 0
    assert all(isinstance(page_data, dict) for page_data in pages_data)
    assert all("path_root" in page_data and "views" in page_data for page_data in pages_data)
    
    # Test Average Duration endpoint
    resp = client.get("/api/v1/admin/analytics/avg-duration", headers=auth_headers)
    assert resp.status_code == 200
    duration_data = resp.json()
    assert isinstance(duration_data, list)
    assert len(duration_data) > 0
    assert all(isinstance(duration, dict) for duration in duration_data)
    assert all("path_root" in duration and "avg_duration" in duration for duration in duration_data)
