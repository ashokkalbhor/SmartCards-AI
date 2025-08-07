from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for system actions
    action_type = Column(String(50), nullable=False)  # create, update, delete, approve, reject
    table_name = Column(String(50), nullable=False)  # users, card_master_data, edit_suggestions, etc.
    record_id = Column(Integer, nullable=True)  # ID of the affected record
    
    # Change details
    old_values = Column(JSON, nullable=True)  # Previous values
    new_values = Column(JSON, nullable=True)  # New values
    change_summary = Column(Text, nullable=True)  # Human-readable summary
    
    # Additional context
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)  # Browser/device info
    session_id = Column(String(100), nullable=True)  # Session identifier
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog(id={self.id}, user_id={self.user_id}, action='{self.action_type}')>"
    
    @property
    def is_system_action(self) -> bool:
        return self.user_id is None
    
    @property
    def is_user_action(self) -> bool:
        return self.user_id is not None 