from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Post Schemas
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=300, description="Post title")
    body: Optional[str] = Field(None, description="Post body content")

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    user_id: int
    card_master_id: int
    user_name: str
    upvotes: int
    downvotes: int
    net_votes: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PostList(BaseModel):
    posts: List[PostResponse]
    total_count: int

# Comment Schemas
class CommentBase(BaseModel):
    body: str = Field(..., min_length=1, description="Comment body")

class CommentCreate(CommentBase):
    parent_id: Optional[int] = Field(None, description="Parent comment ID for nested comments")

class CommentUpdate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    user_id: int
    post_id: int
    parent_id: Optional[int]
    user_name: str
    upvotes: int
    downvotes: int
    net_votes: int
    created_at: datetime
    updated_at: datetime
    replies: List['CommentResponse'] = []
    
    class Config:
        from_attributes = True

# Vote Schemas
class VoteCreate(BaseModel):
    vote_type: str = Field(..., pattern="^(upvote|downvote)$")

class VoteResponse(BaseModel):
    id: int
    user_id: int
    vote_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Post Detail with Comments
class PostDetail(PostResponse):
    comments: List[CommentResponse] = []

# Utility schemas
class TimeAgoResponse(BaseModel):
    time_ago: str
    timestamp: datetime 