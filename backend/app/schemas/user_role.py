from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class UserRoleBase(BaseModel):
    role_type: str = "user"  # user, moderator, admin
    status: str = "active"  # active, inactive, pending


class UserRoleCreate(UserRoleBase):
    user_id: int
    approved_by: Optional[int] = None


class UserRoleUpdate(BaseModel):
    role_type: Optional[str] = None
    status: Optional[str] = None
    approved_by: Optional[int] = None


class UserRoleResponse(UserRoleBase):
    id: int
    user_id: int
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ModeratorRequestBase(BaseModel):
    request_reason: Optional[str] = None
    user_activity_summary: Optional[str] = None


class ModeratorRequestCreate(ModeratorRequestBase):
    user_id: int


class ModeratorRequestUpdate(BaseModel):
    status: str  # pending, approved, rejected
    reviewed_by: Optional[int] = None


class ModeratorRequestResponse(ModeratorRequestBase):
    id: int
    user_id: int
    status: str
    reviewed_by: Optional[int] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserWithRoles(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    roles: List[UserRoleResponse] = []
    moderator_requests: List[ModeratorRequestResponse] = []
    
    class Config:
        from_attributes = True


class AdminUserInfo(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    current_role: Optional[str] = None
    has_moderator_request: bool = False
    moderator_request_status: Optional[str] = None
    
    class Config:
        from_attributes = True 