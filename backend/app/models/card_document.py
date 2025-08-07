from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CardDocument(Base):
    __tablename__ = "card_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_master_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=False)
    
    # Document details
    title = Column(String(200), nullable=False)  # Document title
    description = Column(Text, nullable=True)  # Description of the document
    document_type = Column(String(50), nullable=False)  # link, file, policy_update, terms_change
    content = Column(Text, nullable=False)  # URL for links, file path for uploads, or text content
    
    # File upload details (if applicable)
    file_name = Column(String(255), nullable=True)  # Original filename
    file_size = Column(Integer, nullable=True)  # File size in bytes
    file_type = Column(String(100), nullable=True)  # MIME type
    
    # Status and review
    status = Column(String(20), default="pending")  # pending, approved, rejected
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    review_notes = Column(Text, nullable=True)  # Notes from moderator/admin
    
    # Additional data
    submission_reason = Column(Text, nullable=True)  # Why user submitted this document
    additional_data = Column(JSON, nullable=True)  # Any additional context
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="card_documents")
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    card_master = relationship("CardMasterData", back_populates="card_documents")
    
    def __repr__(self):
        return f"<CardDocument(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
    
    @property
    def is_pending(self) -> bool:
        return self.status == "pending"
    
    @property
    def is_approved(self) -> bool:
        return self.status == "approved"
    
    @property
    def is_rejected(self) -> bool:
        return self.status == "rejected"
    
    @property
    def is_link(self) -> bool:
        return self.document_type == "link"
    
    @property
    def is_file(self) -> bool:
        return self.document_type == "file"
    
    @property
    def is_policy_update(self) -> bool:
        return self.document_type == "policy_update"
    
    @property
    def is_terms_change(self) -> bool:
        return self.document_type == "terms_change" 