from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class CommunityPost(Base):
    __tablename__ = "community_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_master_id = Column(Integer, ForeignKey("card_master_data.id"), nullable=False)
    
    # Post Content
    title = Column(String(300), nullable=False)
    body = Column(Text, nullable=True)
    
    # Metadata
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="community_posts")
    card_master = relationship("CardMasterData", back_populates="community_posts")
    comments = relationship("CommunityComment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("PostVote", back_populates="post", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CommunityPost(id={self.id}, title='{self.title}', user_id={self.user_id})>"
    
    @property
    def net_votes(self) -> int:
        """Calculate net votes (upvotes - downvotes)"""
        return self.upvotes - self.downvotes


class CommunityComment(Base):
    __tablename__ = "community_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("community_comments.id"), nullable=True)  # For nested comments
    
    # Comment Content
    body = Column(Text, nullable=False)
    
    # Metadata
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    is_deleted = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="community_comments")
    post = relationship("CommunityPost", back_populates="comments")
    parent = relationship("CommunityComment", remote_side=[id], back_populates="replies")
    replies = relationship("CommunityComment", back_populates="parent", cascade="all, delete-orphan")
    votes = relationship("CommentVote", back_populates="comment", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CommunityComment(id={self.id}, user_id={self.user_id}, post_id={self.post_id})>"
    
    @property
    def net_votes(self) -> int:
        """Calculate net votes (upvotes - downvotes)"""
        return self.upvotes - self.downvotes


class PostVote(Base):
    __tablename__ = "post_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    vote_type = Column(String(20), nullable=False)  # "upvote" or "downvote"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="post_votes")
    post = relationship("CommunityPost", back_populates="votes")
    
    def __repr__(self):
        return f"<PostVote(user_id={self.user_id}, post_id={self.post_id}, type='{self.vote_type}')>"


class CommentVote(Base):
    __tablename__ = "comment_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("community_comments.id"), nullable=False)
    vote_type = Column(String(20), nullable=False)  # "upvote" or "downvote"
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="comment_votes")
    comment = relationship("CommunityComment", back_populates="votes")
    
    def __repr__(self):
        return f"<CommentVote(user_id={self.user_id}, comment_id={self.comment_id}, type='{self.vote_type}')>" 