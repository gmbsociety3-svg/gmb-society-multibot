"""
Role-Based Access Control (RBAC)
"""

from enum import Enum
from typing import List, Set

class Role(str, Enum):
    """User roles"""
    OWNER = "owner"
    CLIENT = "client"

class Permission(str, Enum):
    """Available permissions"""
    # Owner permissions
    ADD_CLIENT = "add_client"
    REMOVE_CLIENT = "remove_client"
    SUSPEND_CLIENT = "suspend_client"
    REACTIVATE_CLIENT = "reactivate_client"
    ADD_BALANCE = "add_balance"
    DEDUCT_BALANCE = "deduct_balance"
    VIEW_CLIENTS = "view_clients"
    VIEW_BOTS = "view_bots"
    VIEW_STATS = "view_stats"
    VIEW_LOGS = "view_logs"
    MANAGE_LICENSES = "manage_licenses"
    MANAGE_SETTINGS = "manage_settings"
    
    # Client permissions
    VIEW_BALANCE = "view_balance"
    CREATE_BOT = "create_bot"
    VIEW_BOTS_OWN = "view_bots_own"
    RENEW_LICENSE = "renew_license"
    REQUEST_API_CHANGE = "request_api_change"
    VIEW_HISTORY = "view_history"

class PermissionManager:
    """Manage permissions and roles"""
    
    ROLE_PERMISSIONS: dict = {
        Role.OWNER: {
            Permission.ADD_CLIENT,
            Permission.REMOVE_CLIENT,
            Permission.SUSPEND_CLIENT,
            Permission.REACTIVATE_CLIENT,
            Permission.ADD_BALANCE,
            Permission.DEDUCT_BALANCE,
            Permission.VIEW_CLIENTS,
            Permission.VIEW_BOTS,
            Permission.VIEW_STATS,
            Permission.VIEW_LOGS,
            Permission.MANAGE_LICENSES,
            Permission.MANAGE_SETTINGS,
            Permission.CREATE_BOT,
            Permission.VIEW_BALANCE,
            Permission.RENEW_LICENSE,
            Permission.REQUEST_API_CHANGE,
            Permission.VIEW_HISTORY,
        },
        Role.CLIENT: {
            Permission.VIEW_BALANCE,
            Permission.CREATE_BOT,
            Permission.VIEW_BOTS_OWN,
            Permission.RENEW_LICENSE,
            Permission.REQUEST_API_CHANGE,
            Permission.VIEW_HISTORY,
        }
    }
    
    @classmethod
    def has_permission(cls, role: str, permission: str) -> bool:
        """
        Check if role has permission
        
        Args:
            role: User role
            permission: Required permission
        
        Returns:
            True if has permission
        """
        try:
            role_enum = Role(role)
            perm_enum = Permission(permission)
            return perm_enum in cls.ROLE_PERMISSIONS.get(role_enum, set())
        except ValueError:
            return False
    
    @classmethod
    def get_permissions(cls, role: str) -> Set[str]:
        """Get all permissions for a role"""
        try:
            role_enum = Role(role)
            return {p.value for p in cls.ROLE_PERMISSIONS.get(role_enum, set())}
        except ValueError:
            return set()
