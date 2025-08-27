from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, get_async_db
from app.core.security import (
    authenticate_user, authenticate_user_async, create_user, create_user_async,
    create_access_token, create_refresh_token, verify_token, get_current_user_sync
)
from app.models.chat_models import UserLogin, Token, TokenData
from app.core.database import ChatUser
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Login user and return access token"""
    user = await authenticate_user_async(db, user_credentials.username, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "client_id": user.client_id},
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(
        data={"sub": user.user_id, "client_id": user.client_id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/register", response_model=Token)
async def register(
    user_credentials: UserLogin,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Register a new user and return access token"""
    # Check if user already exists
    from sqlalchemy import select
    result = await db.execute(select(ChatUser).where(ChatUser.username == user_credentials.username))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    import uuid
    user_id = str(uuid.uuid4())
    user = await create_user_async(
        db, 
        user_credentials.username, 
        user_credentials.password, 
        user_id
    )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "client_id": user.client_id},
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token = create_refresh_token(
        data={"sub": user.user_id, "client_id": user.client_id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_async_db)
) -> Any:
    """Refresh access token using refresh token"""
    # Verify refresh token
    token_data = verify_token(refresh_token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user
    from sqlalchemy import select
    result = await db.execute(select(ChatUser).where(ChatUser.user_id == token_data.user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create new access token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_id, "client_id": user.client_id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
async def get_current_user_info(
    current_user: ChatUser = Depends(get_current_user_sync)
) -> Any:
    """Get current user information"""
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "client_id": current_user.client_id,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    }

@router.post("/logout")
async def logout(
    current_user: ChatUser = Depends(get_current_user_sync)
) -> Any:
    """Logout user (invalidate session)"""
    # In a real implementation, you might want to blacklist the token
    # For now, we'll just return success
    return {"message": "Successfully logged out"}
