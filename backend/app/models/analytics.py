from sqlalchemy import Column, Integer, String, DateTime, Text, func
from app.core.database import Base

class AnalyticsEvent(Base):
    __tablename__ = 'analytics_events'

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(64), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    path_root = Column(String(64), nullable=False, index=True)
    duration_seconds = Column(Integer, nullable=True)
    properties = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
