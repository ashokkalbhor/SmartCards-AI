from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.card_document import CardDocument
from app.models.card_master_data import CardMasterData
from app.models.audit_log import AuditLog
from app.schemas.card_document import (
    CardDocumentResponse, CardDocumentSummary, CardDocumentStats,
    CardDocumentSubmissionRequest
)

router = APIRouter()


@router.post("/submit")
async def submit_card_document(
    card_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    document_type: str = Form(...),  # link, file, policy_update, terms_change
    content: str = Form(...),  # URL for links, text for policy updates
    submission_reason: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a document/link for a card"""
    # Verify card exists
    card = db.query(CardMasterData).filter(CardMasterData.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    # Validate document type
    valid_types = ["link", "file", "policy_update", "terms_change"]
    if document_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid document type. Must be one of: {', '.join(valid_types)}"
        )
    
    # Handle file upload if document_type is "file"
    file_name = None
    file_size = None
    file_type = None
    
    if document_type == "file":
        if not file:
            raise HTTPException(
                status_code=400,
                detail="File is required for document type 'file'"
            )
        
        # Validate file type
        allowed_types = ["application/pdf", "image/jpeg", "image/png", "image/gif", "text/plain"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Validate file size (5MB limit)
        if file.size > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size too large. Maximum size is 5MB"
            )
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_size = file.size
        file_type = file.content_type
        
        # Save file
        upload_dir = "uploads/card_documents"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file_name)
        
        with open(file_path, "wb") as buffer:
            content_data = await file.read()
            buffer.write(content_data)
        
        # Update content to file path
        content = file_path
    
    # Check if similar submission already exists
    existing_submission = db.query(CardDocument).filter(
        CardDocument.user_id == current_user.id,
        CardDocument.card_master_id == card_id,
        CardDocument.title == title,
        CardDocument.status == "pending"
    ).first()
    
    if existing_submission:
        raise HTTPException(
            status_code=400,
            detail="You already have a pending submission with this title for this card"
        )
    
    # Create card document
    card_document = CardDocument(
        user_id=current_user.id,
        card_master_id=card_id,
        title=title,
        description=description,
        document_type=document_type,
        content=content,
        submission_reason=submission_reason,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type,
        status="pending"
    )
    
    db.add(card_document)
    db.commit()
    db.refresh(card_document)
    
    return {"message": "Document submission successful"}


@router.get("/my-submissions", response_model=List[CardDocumentResponse])
def get_my_submissions(
    status_filter: Optional[str] = Query(None, regex="^(pending|approved|rejected)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current user's document submissions"""
    query = db.query(CardDocument).filter(CardDocument.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(CardDocument.status == status_filter)
    
    submissions = query.order_by(desc(CardDocument.created_at)).offset(skip).limit(limit).all()
    
    # Add user and card information
    result = []
    for submission in submissions:
        card = db.query(CardMasterData).filter(CardMasterData.id == submission.card_master_id).first()
        
        submission_dict = CardDocumentResponse.from_orm(submission)
        submission_dict.user_name = current_user.full_name
        submission_dict.card_name = card.card_name if card else "Unknown Card"
        submission_dict.bank_name = card.bank_name if card else "Unknown Bank"
        
        result.append(submission_dict)
    
    return result


@router.get("/my-submissions/stats")
def get_my_submissions_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get statistics for current user's submissions"""
    total_pending = db.query(func.count(CardDocument.id)).filter(
        CardDocument.user_id == current_user.id,
        CardDocument.status == "pending"
    ).scalar()
    
    total_approved = db.query(func.count(CardDocument.id)).filter(
        CardDocument.user_id == current_user.id,
        CardDocument.status == "approved"
    ).scalar()
    
    total_rejected = db.query(func.count(CardDocument.id)).filter(
        CardDocument.user_id == current_user.id,
        CardDocument.status == "rejected"
    ).scalar()
    
    # Count by document type
    pending_by_type = {}
    for doc_type in ["link", "file", "policy_update", "terms_change"]:
        count = db.query(func.count(CardDocument.id)).filter(
            CardDocument.user_id == current_user.id,
            CardDocument.status == "pending",
            CardDocument.document_type == doc_type
        ).scalar()
        pending_by_type[doc_type] = count
    
    return CardDocumentStats(
        total_pending=total_pending,
        total_approved=total_approved,
        total_rejected=total_rejected,
        pending_by_type=pending_by_type
    )


@router.get("/approved/{card_id}", response_model=List[CardDocumentResponse])
def get_approved_documents(
    card_id: int,
    db: Session = Depends(get_db)
):
    """Get approved documents for a specific card"""
    documents = db.query(CardDocument).filter(
        CardDocument.card_master_id == card_id,
        CardDocument.status == "approved"
    ).order_by(desc(CardDocument.created_at)).all()
    
    # Add user and card information
    result = []
    for document in documents:
        user = db.query(User).filter(User.id == document.user_id).first()
        card = db.query(CardMasterData).filter(CardMasterData.id == document.card_master_id).first()
        
        document_dict = CardDocumentResponse.from_orm(document)
        document_dict.user_name = user.full_name if user else "Unknown User"
        document_dict.card_name = card.card_name if card else "Unknown Card"
        document_dict.bank_name = card.bank_name if card else "Unknown Bank"
        
        result.append(document_dict)
    
    return result 