from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class EditSuggestion(Base):
    __tablename__ = "edit_suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    moderator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    card_master_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=False)
    
    # Suggestion details
    field_type = Column(String(50), nullable=False)  # spending_category, merchant_reward
    field_name = Column(String(100), nullable=False)  # category name or merchant name
    old_value = Column(Text, nullable=True)  # Current value
    new_value = Column(Text, nullable=False)  # Proposed new value
    
    # Status and review
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    review_notes = Column(Text, nullable=True)  # Notes from moderator/admin
    
    # Additional data
    suggestion_reason = Column(Text, nullable=True)  # Why user suggested this change
    additional_data = Column(JSON, nullable=True)  # Any additional context
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="edit_suggestions")
    moderator = relationship("User", foreign_keys=[moderator_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    card_master = relationship("CardMasterData", back_populates="edit_suggestions")
    
    def __repr__(self):
        return f"<EditSuggestion(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
    
    @property
    def is_pending(self) -> bool:
        return self.status == "pending"
    
    @property
    def is_approved(self) -> bool:
        return self.status == "approved"
    
    @property
    def is_rejected(self) -> bool:
        return self.status == "rejected" 