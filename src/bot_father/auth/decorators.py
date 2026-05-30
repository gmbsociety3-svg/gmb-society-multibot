"""
Authorization Decorators
"""

from functools import wraps
from typing import Callable
from src.utils.exceptions import AuthorizationException
from src.bot_father.auth.permissions import PermissionManager

def require_owner(func: Callable) -> Callable:
    """
    Decorator to require owner role
    
    Usage:
        @require_owner
        def some_function(context):
            pass
    """
    @wraps(func)
    async def wrapper(self, update, context, *args, **kwargs):
        user_role = context.user_data.get("role")
        if user_role != "owner":
            raise AuthorizationException("❌ Only owner can access this feature")
        return await func(self, update, context, *args, **kwargs)
    return wrapper

def require_permission(permission: str) -> Callable:
    """
    Decorator to require specific permission
    
    Usage:
        @require_permission("add_balance")
        def add_balance(context):
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, update, context, *args, **kwargs):
            user_role = context.user_data.get("role")
            if not PermissionManager.has_permission(user_role, permission):
                raise AuthorizationException(
                    f"❌ You don't have permission to: {permission}"
                )
            return await func(self, update, context, *args, **kwargs)
        return wrapper
    return decorator
