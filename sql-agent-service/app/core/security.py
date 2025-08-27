from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .config import settings
from .database import get_db, get_async_db, ChatUser
from ..models.chat_models import TokenData

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        client_id: str = payload.get("client_id")
        
        if user_id is None:
            return None
        
        return TokenData(user_id=user_id, client_id=client_id)
    except JWTError:
        return None

def get_current_user_sync(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> ChatUser:
    """Get current user from JWT token (synchronous)"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user = db.query(ChatUser).filter(ChatUser.user_id == token_data.user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_current_user_async(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_async_db)) -> ChatUser:
    """Get current user from JWT token (asynchronous)"""
    token = credentials.credentials
    token_data = verify_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    result = await db.execute(select(ChatUser).where(ChatUser.user_id == token_data.user_id))
    user = result.scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def authenticate_user(db: Session, username: str, password: str) -> Optional[ChatUser]:
    """Authenticate a user with username and password"""
    user = db.query(ChatUser).filter(ChatUser.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def authenticate_user_async(db: AsyncSession, username: str, password: str) -> Optional[ChatUser]:
    """Authenticate a user with username and password (async)"""
    result = await db.execute(select(ChatUser).where(ChatUser.username == username))
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, username: str, password: str, user_id: str, client_id: Optional[str] = None) -> ChatUser:
    """Create a new user"""
    hashed_password = get_password_hash(password)
    db_user = ChatUser(
        username=username,
        hashed_password=hashed_password,
        user_id=user_id,
        client_id=client_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def create_user_async(db: AsyncSession, username: str, password: str, user_id: str, client_id: Optional[str] = None) -> ChatUser:
    """Create a new user (async)"""
    hashed_password = get_password_hash(password)
    db_user = ChatUser(
        username=username,
        hashed_password=hashed_password,
        user_id=user_id,
        client_id=client_id
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
