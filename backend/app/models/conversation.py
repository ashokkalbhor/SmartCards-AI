from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Conversation Information
    title = Column(String(200), nullable=True)
    conversation_type = Column(String(50), default="card_recommendation")  # card_recommendation, general_help, etc.
    status = Column(String(20), default="active")  # active, completed, archived
    
    # Context and Preferences
    user_preferences = Column(JSON, nullable=True)  # User's card preferences, spending patterns
    conversation_context = Column(JSON, nullable=True)  # AI context, previous recommendations
    
    # Metrics
    message_count = Column(Integer, default=0)
    total_tokens_used = Column(Integer, default=0)
    ai_response_time_avg = Column(Float, nullable=True)  # Average response time in seconds
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, type='{self.conversation_type}')>"
    
    def to_dict(self):
        """Convert conversation to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "conversation_type": self.conversation_type,
            "status": self.status,
            "user_preferences": self.user_preferences,
            "conversation_context": self.conversation_context,
            "message_count": self.message_count,
            "total_tokens_used": self.total_tokens_used,
            "ai_response_time_avg": self.ai_response_time_avg,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_message_at": self.last_message_at.isoformat() if self.last_message_at else None,
        }


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    
    # Message Information
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    message_type = Column(String(50), default="text")  # text, card_recommendation, spending_analysis, etc.
    
    # AI-specific fields
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    response_time = Column(Float, nullable=True)  # Response time in seconds
    
    # Metadata
    message_metadata = Column(JSON, nullable=True)  # Additional data like card recommendations, analysis results
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<ConversationMessage(id={self.id}, conversation_id={self.conversation_id}, role='{self.role}')>"
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "role": self.role,
            "content": self.content,
            "message_type": self.message_type,
            "tokens_used": self.tokens_used,
            "model_used": self.model_used,
            "response_time": self.response_time,
            "message_metadata": self.message_metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class CardRecommendation(Base):
    __tablename__ = "card_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Recommendation Information
    card_name = Column(String(200), nullable=False)
    card_type = Column(String(50), nullable=False)
    card_network = Column(String(50), nullable=False)
    
    # Recommendation Details
    recommendation_reason = Column(Text, nullable=False)
    expected_rewards = Column(Float, nullable=True)
    annual_fee = Column(Float, nullable=True)
    credit_score_requirement = Column(Integer, nullable=True)
    
    # User's spending categories and expected benefits
    spending_categories = Column(JSON, nullable=True)  # Categories where this card excels
    category_reward_rates = Column(JSON, nullable=True)  # Reward rates for different categories
    
    # Recommendation Status
    status = Column(String(20), default="recommended")  # recommended, applied, rejected, approved
    user_feedback = Column(String(20), nullable=True)  # like, dislike, neutral
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    conversation = relationship("Conversation")
    user = relationship("User")
    
    def __repr__(self):
        return f"<CardRecommendation(id={self.id}, card_name='{self.card_name}', user_id={self.user_id})>"
    
    def to_dict(self):
        """Convert recommendation to dictionary"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "card_name": self.card_name,
            "card_type": self.card_type,
            "card_network": self.card_network,
            "recommendation_reason": self.recommendation_reason,
            "expected_rewards": self.expected_rewards,
            "annual_fee": self.annual_fee,
            "credit_score_requirement": self.credit_score_requirement,
            "spending_categories": self.spending_categories,
            "category_reward_rates": self.category_reward_rates,
            "status": self.status,
            "user_feedback": self.user_feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 