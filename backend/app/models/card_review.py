from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base

class CardReview(Base):
    __tablename__ = "card_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_master_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=False)
    
    # Rating
    overall_rating = Column(Integer, nullable=False)  # 1-5 stars
    
    # Review Content
    review_title = Column(String(200), nullable=True)
    review_content = Column(Text, nullable=True)
    pros = Column(Text, nullable=True)
    cons = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    
    # Metadata
    is_verified_cardholder = Column(Boolean, default=False)
    helpful_votes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="card_reviews")
    card_master = relationship("CardMasterData", back_populates="reviews")
    votes = relationship("ReviewVote", back_populates="review", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CardReview(id={self.id}, user_id={self.user_id}, card_id={self.card_master_id})>"

class ReviewVote(Base):
    __tablename__ = "review_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    review_id = Column(Integer, ForeignKey("card_reviews.id"), nullable=False)
    vote_type = Column(String(20), nullable=False)  # 'helpful' or 'not_helpful'
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="review_votes")
    review = relationship("CardReview", back_populates="votes")
    
    def __repr__(self):
        return f"<ReviewVote(id={self.id}, user_id={self.user_id}, review_id={self.review_id})>" 