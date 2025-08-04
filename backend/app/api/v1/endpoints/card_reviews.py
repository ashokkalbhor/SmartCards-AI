from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.card_review import CardReview, ReviewVote
from app.models.card_master_data import CardMasterData
from app.schemas.card_review import (
    CardReviewCreate, 
    CardReviewResponse, 
    CardReviewList,
    ReviewVoteCreate,
    ReviewVoteResponse
)

router = APIRouter()

@router.get("/cards/{card_id}/reviews", response_model=CardReviewList)
def get_card_reviews(
    card_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get reviews for a specific card"""
    # Check if card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Get reviews
    reviews_query = db.query(CardReview).filter(CardReview.card_master_id == card_id)
    total_count = reviews_query.count()
    
    reviews = reviews_query.offset(skip).limit(limit).all()
    
    # Calculate average rating
    avg_rating = db.query(func.avg(CardReview.overall_rating)).filter(
        CardReview.card_master_id == card_id
    ).scalar() or 0.0
    
    # Convert to response format
    review_responses = []
    for review in reviews:
        review_responses.append(CardReviewResponse(
            id=review.id,
            user_id=review.user_id,
            card_master_id=review.card_master_id,
            user_name=f"{review.user.first_name} {review.user.last_name}".strip(),
            overall_rating=review.overall_rating,
            review_title=review.review_title,
            review_content=review.review_content,
            pros=review.pros,
            cons=review.cons,
            experience=review.experience,
            is_verified_cardholder=review.is_verified_cardholder,
            helpful_votes=review.helpful_votes,
            created_at=review.created_at,
            updated_at=review.updated_at or review.created_at  # Use created_at as fallback if updated_at is None
        ))
    
    return CardReviewList(
        reviews=review_responses,
        total_count=total_count,
        average_rating=float(avg_rating)
    )

@router.post("/cards/{card_id}/reviews", response_model=CardReviewResponse)
def create_card_review(
    card_id: int,
    review_data: CardReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new review for a card"""
    # Check if card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Check if user already reviewed this card
    existing_review = db.query(CardReview).filter(
        CardReview.user_id == current_user.id,
        CardReview.card_master_id == card_id
    ).first()
    
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this card")
    
    # Create review
    review = CardReview(
        user_id=current_user.id,
        card_master_id=card_id,
        overall_rating=review_data.overall_rating,
        review_title=review_data.review_title,
        review_content=review_data.review_content,
        pros=review_data.pros,
        cons=review_data.cons,
        experience=review_data.experience
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return CardReviewResponse(
        id=review.id,
        user_id=review.user_id,
        card_master_id=review.card_master_id,
        user_name=f"{current_user.first_name} {current_user.last_name}".strip(),
        overall_rating=review.overall_rating,
        review_title=review.review_title,
        review_content=review.review_content,
        pros=review.pros,
        cons=review.cons,
        experience=review.experience,
        is_verified_cardholder=review.is_verified_cardholder,
        helpful_votes=review.helpful_votes,
        created_at=review.created_at,
        updated_at=review.updated_at or review.created_at  # Use created_at as fallback if updated_at is None
    )

@router.put("/reviews/{review_id}", response_model=CardReviewResponse)
def update_card_review(
    review_id: int,
    review_data: CardReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing review"""
    # Get the review
    review = db.query(CardReview).filter(CardReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user owns this review
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own reviews")
    
    # Update review
    review.overall_rating = review_data.overall_rating
    review.review_title = review_data.review_title
    review.review_content = review_data.review_content
    review.pros = review_data.pros
    review.cons = review_data.cons
    review.experience = review_data.experience
    
    db.commit()
    db.refresh(review)
    
    return CardReviewResponse(
        id=review.id,
        user_id=review.user_id,
        card_master_id=review.card_master_id,
        user_name=f"{current_user.first_name} {current_user.last_name}".strip(),
        overall_rating=review.overall_rating,
        review_title=review.review_title,
        review_content=review.review_content,
        pros=review.pros,
        cons=review.cons,
        experience=review.experience,
        is_verified_cardholder=review.is_verified_cardholder,
        helpful_votes=review.helpful_votes,
        created_at=review.created_at,
        updated_at=review.updated_at
    )

@router.delete("/reviews/{review_id}")
def delete_card_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a review"""
    # Get the review
    review = db.query(CardReview).filter(CardReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user owns this review
    if review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own reviews")
    
    db.delete(review)
    db.commit()
    
    return {"message": "Review deleted successfully"}

@router.post("/reviews/{review_id}/vote", response_model=ReviewVoteResponse)
def vote_on_review(
    review_id: int,
    vote_data: ReviewVoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Vote on a review (helpful/not helpful)"""
    # Check if review exists
    review = db.query(CardReview).filter(CardReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if user already voted on this review
    existing_vote = db.query(ReviewVote).filter(
        ReviewVote.user_id == current_user.id,
        ReviewVote.review_id == review_id
    ).first()
    
    if existing_vote:
        # Update existing vote
        existing_vote.vote_type = vote_data.vote_type
        db.commit()
        db.refresh(existing_vote)
        vote = existing_vote
    else:
        # Create new vote
        vote = ReviewVote(
            user_id=current_user.id,
            review_id=review_id,
            vote_type=vote_data.vote_type
        )
        db.add(vote)
        db.commit()
        db.refresh(vote)
    
    # Update helpful votes count on the review
    helpful_votes = db.query(ReviewVote).filter(
        ReviewVote.review_id == review_id,
        ReviewVote.vote_type == "helpful"
    ).count()
    
    review.helpful_votes = helpful_votes
    db.commit()
    
    return ReviewVoteResponse(
        id=vote.id,
        user_id=vote.user_id,
        review_id=vote.review_id,
        vote_type=vote.vote_type,
        created_at=vote.created_at
    ) 