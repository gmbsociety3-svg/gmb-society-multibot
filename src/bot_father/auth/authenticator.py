"""
Bot Father Authenticator
Manages owner and client authentication
"""

import logging
from typing import Optional, Tuple
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.utils.exceptions import (
    AuthenticationException,
    AuthorizationException,
    UserNotFoundException
)

logger = logging.getLogger(__name__)

class Authenticator:
    """Handle authentication for Bot Father"""
    
    def __init__(self, db: DatabaseManager, owner_id: int):
        """
        Initialize authenticator
        
        Args:
            db: Database manager instance
            owner_id: Telegram ID of the owner
        """
        self.db = db
        self.owner_id = owner_id
    
    def is_owner(self, telegram_id: int) -> bool:
        """Check if user is owner"""
        return telegram_id == self.owner_id
    
    def is_registered_client(self, telegram_id: int) -> bool:
        """Check if user is registered client"""
        users = self.db.query("users", {"telegram_id": telegram_id})
        return len(users) > 0 and users[0].get("role") == "client"
    
    def authenticate_user(self, telegram_id: int) -> Tuple[bool, Optional[dict]]:
        """
        Authenticate a user (owner or client)
        
        Args:
            telegram_id: User's telegram ID
        
        Returns:
            Tuple of (is_authenticated, user_data)
        """
        # Check if owner
        if self.is_owner(telegram_id):
            return True, {"telegram_id": telegram_id, "role": "owner"}
        
        # Check if registered client
        users = self.db.query("users", {"telegram_id": telegram_id})
        
        if not users:
            return False, None
        
        user = users[0]
        
        # Check if active
        if user.get("status") != "active":
            return False, None
        
        # Update last login
        self.db.update("users", user["id"], {
            "last_login": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Client authenticated: {telegram_id}")
        return True, user
    
    def register_client(self, telegram_id: int, username: str) -> str:
        """
        Register a new client (Owner only)
        
        Args:
            telegram_id: Client's telegram ID
            username: Client's username
        
        Returns:
            User ID
        
        Raises:
            AuthorizationException: If already registered
        """
        # Check if already registered
        existing = self.db.query("users", {"telegram_id": telegram_id})
        if existing:
            raise AuthorizationException("User already registered")
        
        user_data = {
            "telegram_id": telegram_id,
            "username": username,
            "role": "client",
            "balance": 0.0,
            "status": "active",
            "bots_created": 0,
            "api_key_changes": 0,
            "last_login": None
        }
        
        user_id = self.db.create("users", user_data)
        logger.info(f"Client registered: {telegram_id} (ID: {user_id})")
        
        return user_id
    
    def suspend_user(self, user_id: str) -> bool:
        """Suspend a client account"""
        result = self.db.update("users", user_id, {"status": "suspended"})
        if result:
            logger.info(f"User suspended: {user_id}")
        return result
    
    def reactivate_user(self, user_id: str) -> bool:
        """Reactivate a client account"""
        result = self.db.update("users", user_id, {"status": "active"})
        if result:
            logger.info(f"User reactivated: {user_id}")
        return result
    
    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user by ID"""
        return self.db.read("users", user_id)
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[dict]:
        """Get user by Telegram ID"""
        users = self.db.query("users", {"telegram_id": telegram_id})
        return users[0] if users else None
