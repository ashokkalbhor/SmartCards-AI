from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.community import CommunityPost, CommunityComment, PostVote, CommentVote
from app.models.card_master_data import CardMasterData
from app.schemas.community import (
    PostCreate, PostUpdate, PostResponse, PostList, PostDetail,
    CommentCreate, CommentUpdate, CommentResponse,
    VoteCreate, VoteResponse
)

router = APIRouter()

def format_time_ago(timestamp: datetime) -> str:
    """Format timestamp as 'time ago' string"""
    now = datetime.utcnow()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days}d ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    else:
        return "just now"

def build_comment_tree(comments: List[CommunityComment]) -> List[CommentResponse]:
    """Build nested comment tree structure"""
    comment_dict = {comment.id: comment for comment in comments}
    root_comments = []
    
    for comment in comments:
        if comment.parent_id is None:
            # Root comment
            root_comments.append(comment)
        else:
            # Child comment
            parent = comment_dict.get(comment.parent_id)
            if parent:
                if not hasattr(parent, 'replies'):
                    parent.replies = []
                parent.replies.append(comment)
    
    def convert_to_response(comment: CommunityComment) -> CommentResponse:
        replies = [convert_to_response(reply) for reply in getattr(comment, 'replies', [])]
        return CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            post_id=comment.post_id,
            parent_id=comment.parent_id,
            user_name=comment.user.full_name,
            body=comment.body,
            upvotes=comment.upvotes,
            downvotes=comment.downvotes,
            net_votes=comment.net_votes,
            created_at=comment.created_at,
            updated_at=comment.updated_at or comment.created_at,
            replies=replies
        )
    
    return [convert_to_response(comment) for comment in root_comments]

# Post endpoints
@router.get("/cards/{card_id}/posts", response_model=PostList)
def get_card_posts(
    card_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("newest", regex="^(newest|oldest|votes)$"),
    db: Session = Depends(get_db)
):
    """Get posts for a specific card with sorting options"""
    # Check if card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Build query
    query = db.query(CommunityPost).filter(
        CommunityPost.card_master_id == card_id,
        CommunityPost.is_deleted == False
    )
    
    # Apply sorting
    if sort_by == "newest":
        query = query.order_by(desc(CommunityPost.created_at))
    elif sort_by == "oldest":
        query = query.order_by(asc(CommunityPost.created_at))
    elif sort_by == "votes":
        query = query.order_by(desc(CommunityPost.upvotes - CommunityPost.downvotes))
    
    total_count = query.count()
    posts = query.offset(skip).limit(limit).all()
    
    # Convert to response format
    post_responses = []
    for post in posts:
        post_responses.append(PostResponse(
            id=post.id,
            user_id=post.user_id,
            card_master_id=post.card_master_id,
            user_name=post.user.full_name,
            title=post.title,
            body=post.body,
            upvotes=post.upvotes,
            downvotes=post.downvotes,
            net_votes=post.net_votes,
            comment_count=post.comment_count,
            created_at=post.created_at,
            updated_at=post.updated_at or post.created_at
        ))
    
    return PostList(posts=post_responses, total_count=total_count)

@router.post("/cards/{card_id}/posts", response_model=PostResponse)
def create_post(
    card_id: int,
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new post for a card"""
    # Check if card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Create post
    post = CommunityPost(
        user_id=current_user.id,
        card_master_id=card_id,
        title=post_data.title,
        body=post_data.body
    )
    
    db.add(post)
    db.commit()
    db.refresh(post)
    
    return PostResponse(
        id=post.id,
        user_id=post.user_id,
        card_master_id=post.card_master_id,
        user_name=post.user.full_name,
        title=post.title,
        body=post.body,
        upvotes=post.upvotes,
        downvotes=post.downvotes,
        net_votes=post.net_votes,
        comment_count=post.comment_count,
        created_at=post.created_at,
        updated_at=post.updated_at or post.created_at
    )

@router.get("/posts/{post_id}", response_model=PostDetail)
def get_post_detail(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed post with all comments"""
    post = db.query(CommunityPost).filter(
        CommunityPost.id == post_id,
        CommunityPost.is_deleted == False
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Get all comments for this post
    comments = db.query(CommunityComment).filter(
        CommunityComment.post_id == post_id,
        CommunityComment.is_deleted == False
    ).order_by(asc(CommunityComment.created_at)).all()
    
    # Build comment tree
    comment_tree = build_comment_tree(comments)
    
    return PostDetail(
        id=post.id,
        user_id=post.user_id,
        card_master_id=post.card_master_id,
        user_name=post.user.full_name,
        title=post.title,
        body=post.body,
        upvotes=post.upvotes,
        downvotes=post.downvotes,
        net_votes=post.net_votes,
        comment_count=post.comment_count,
        created_at=post.created_at,
        updated_at=post.updated_at or post.created_at,
        comments=comment_tree
    )

@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a post (only by the author)"""
    post = db.query(CommunityPost).filter(
        CommunityPost.id == post_id,
        CommunityPost.is_deleted == False
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this post")
    
    # Update post
    post.title = post_data.title
    post.body = post_data.body
    post.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(post)
    
    return PostResponse(
        id=post.id,
        user_id=post.user_id,
        card_master_id=post.card_master_id,
        user_name=post.user.full_name,
        title=post.title,
        body=post.body,
        upvotes=post.upvotes,
        downvotes=post.downvotes,
        net_votes=post.net_votes,
        comment_count=post.comment_count,
        created_at=post.created_at,
        updated_at=post.updated_at or post.created_at
    )

@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a post (only by the author)"""
    post = db.query(CommunityPost).filter(
        CommunityPost.id == post_id,
        CommunityPost.is_deleted == False
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    # Soft delete
    post.is_deleted = True
    db.commit()
    
    return {"message": "Post deleted successfully"}

# Comment endpoints
@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new comment on a post"""
    # Check if post exists
    post = db.query(CommunityPost).filter(
        CommunityPost.id == post_id,
        CommunityPost.is_deleted == False
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if parent comment exists (if provided)
    if comment_data.parent_id:
        parent_comment = db.query(CommunityComment).filter(
            CommunityComment.id == comment_data.parent_id,
            CommunityComment.post_id == post_id,
            CommunityComment.is_deleted == False
        ).first()
        
        if not parent_comment:
            raise HTTPException(status_code=404, detail="Parent comment not found")
    
    # Create comment
    comment = CommunityComment(
        user_id=current_user.id,
        post_id=post_id,
        parent_id=comment_data.parent_id,
        body=comment_data.body
    )
    
    db.add(comment)
    
    # Update post comment count
    post.comment_count += 1
    
    db.commit()
    db.refresh(comment)
    
    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        post_id=comment.post_id,
        parent_id=comment.parent_id,
        user_name=comment.user.full_name,
        body=comment.body,
        upvotes=comment.upvotes,
        downvotes=comment.downvotes,
        net_votes=comment.net_votes,
        created_at=comment.created_at,
        updated_at=comment.updated_at or comment.created_at,
        replies=[]
    )

@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a comment (only by the author)"""
    comment = db.query(CommunityComment).filter(
        CommunityComment.id == comment_id,
        CommunityComment.is_deleted == False
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    
    # Update comment
    comment.body = comment_data.body
    comment.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(comment)
    
    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        post_id=comment.post_id,
        parent_id=comment.parent_id,
        user_name=comment.user.full_name,
        body=comment.body,
        upvotes=comment.upvotes,
        downvotes=comment.downvotes,
        net_votes=comment.net_votes,
        created_at=comment.created_at,
        updated_at=comment.updated_at or comment.created_at,
        replies=[]
    )

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a comment (only by the author)"""
    comment = db.query(CommunityComment).filter(
        CommunityComment.id == comment_id,
        CommunityComment.is_deleted == False
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    # Soft delete
    comment.is_deleted = True
    
    # Update post comment count
    post = db.query(CommunityPost).filter(CommunityPost.id == comment.post_id).first()
    if post:
        post.comment_count = max(0, post.comment_count - 1)
    
    db.commit()
    
    return {"message": "Comment deleted successfully"}

# Voting endpoints
@router.post("/posts/{post_id}/vote", response_model=VoteResponse)
def vote_on_post(
    post_id: int,
    vote_data: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Vote on a post"""
    post = db.query(CommunityPost).filter(
        CommunityPost.id == post_id,
        CommunityPost.is_deleted == False
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if user already voted
    existing_vote = db.query(PostVote).filter(
        PostVote.user_id == current_user.id,
        PostVote.post_id == post_id
    ).first()
    
    if existing_vote:
        # Update existing vote
        if existing_vote.vote_type == vote_data.vote_type:
            # Remove vote if same type
            db.delete(existing_vote)
            if vote_data.vote_type == "upvote":
                post.upvotes = max(0, post.upvotes - 1)
            else:
                post.downvotes = max(0, post.downvotes - 1)
        else:
            # Change vote type
            if existing_vote.vote_type == "upvote":
                post.upvotes = max(0, post.upvotes - 1)
                post.downvotes += 1
            else:
                post.downvotes = max(0, post.downvotes - 1)
                post.upvotes += 1
            existing_vote.vote_type = vote_data.vote_type
    else:
        # Create new vote
        vote = PostVote(
            user_id=current_user.id,
            post_id=post_id,
            vote_type=vote_data.vote_type
        )
        db.add(vote)
        
        if vote_data.vote_type == "upvote":
            post.upvotes += 1
        else:
            post.downvotes += 1
    
    db.commit()
    
    return VoteResponse(
        id=existing_vote.id if existing_vote else vote.id,
        user_id=current_user.id,
        vote_type=vote_data.vote_type,
        created_at=existing_vote.created_at if existing_vote else vote.created_at
    )

@router.post("/comments/{comment_id}/vote", response_model=VoteResponse)
def vote_on_comment(
    comment_id: int,
    vote_data: VoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Vote on a comment"""
    comment = db.query(CommunityComment).filter(
        CommunityComment.id == comment_id,
        CommunityComment.is_deleted == False
    ).first()
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Check if user already voted
    existing_vote = db.query(CommentVote).filter(
        CommentVote.user_id == current_user.id,
        CommentVote.comment_id == comment_id
    ).first()
    
    if existing_vote:
        # Update existing vote
        if existing_vote.vote_type == vote_data.vote_type:
            # Remove vote if same type
            db.delete(existing_vote)
            if vote_data.vote_type == "upvote":
                comment.upvotes = max(0, comment.upvotes - 1)
            else:
                comment.downvotes = max(0, comment.downvotes - 1)
        else:
            # Change vote type
            if existing_vote.vote_type == "upvote":
                comment.upvotes = max(0, comment.upvotes - 1)
                comment.downvotes += 1
            else:
                comment.downvotes = max(0, comment.downvotes - 1)
                comment.upvotes += 1
            existing_vote.vote_type = vote_data.vote_type
    else:
        # Create new vote
        vote = CommentVote(
            user_id=current_user.id,
            comment_id=comment_id,
            vote_type=vote_data.vote_type
        )
        db.add(vote)
        
        if vote_data.vote_type == "upvote":
            comment.upvotes += 1
        else:
            comment.downvotes += 1
    
    db.commit()
    
    return VoteResponse(
        id=existing_vote.id if existing_vote else vote.id,
        user_id=current_user.id,
        vote_type=vote_data.vote_type,
        created_at=existing_vote.created_at if existing_vote else vote.created_at
    ) 