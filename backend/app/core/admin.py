from typing import List
from app.core.config import settings
from app.models.user import User


def is_admin(user: User) -> bool:
    """Check if user is an admin"""
    return user.email in settings.ADMIN_EMAILS


def is_moderator(user: User) -> bool:
    """Check if user is a moderator"""
    return user.role == "moderator" or is_admin(user)


def get_admin_emails() -> List[str]:
    """Get list of admin emails"""
    return settings.ADMIN_EMAILS


def can_approve_suggestions(user: User) -> bool:
    """Check if user can approve suggestions"""
    return is_moderator(user)


def can_manage_users(user: User) -> bool:
    """Check if user can manage other users"""
    return is_admin(user)


def can_edit_cards(user: User) -> bool:
    """Check if user can directly edit card data"""
    return is_moderator(user) 