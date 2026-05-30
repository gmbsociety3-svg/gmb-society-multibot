"""
User Management Service
Handle client registration, suspension, and user operations
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.utils.exceptions import UserNotFoundException, ValidationException
from src.utils.validators import Validators

logger = logging.getLogger(__name__)

class UserService:
    """Manage user operations"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def register_client(self, telegram_id: int, username: str) -> str:
        """
        Register a new client
        
        Args:
            telegram_id: Client's Telegram ID
            username: Client's username
        
        Returns:
            User ID
        
        Raises:
            ValidationException: If data invalid
        """
        # Validate inputs
        is_valid, error = Validators.validate_telegram_id(telegram_id)
        if not is_valid:
            raise ValidationException(f"Invalid Telegram ID: {error}")
        
        is_valid, error = Validators.validate_username(username)
        if not is_valid:
            raise ValidationException(f"Invalid username: {error}")
        
        # Check if already exists
        existing = self.db.query("users", {"telegram_id": telegram_id})
        if existing:
            raise ValidationException("User already registered")
        
        user_data = {
            "telegram_id": telegram_id,
            "username": username,
            "role": "client",
            "balance": 0.0,
            "status": "active",
            "bots_created": 0,
            "api_key_changes": 0,
            "last_login": None,
            "created_at": datetime.utcnow().isoformat(),
        }
        
        user_id = self.db.create("users", user_data)
        logger.info(f"Client registered: {telegram_id} (ID: {user_id})")
        
        return user_id
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.db.read("users", user_id)
        if not user:
            raise UserNotFoundException(f"User not found: {user_id}")
        return user
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """Get user by Telegram ID"""
        users = self.db.query("users", {"telegram_id": telegram_id})
        if not users:
            return None
        return users[0]
    
    def list_all_clients(self) -> List[Dict[str, Any]]:
        """List all registered clients"""
        all_users = self.db.list_all("users")
        return [u for u in all_users if u.get("role") == "client"]
    
    def suspend_user(self, user_id: str) -> bool:
        """Suspend a client"""
        user = self.get_user(user_id)
        if user.get("status") == "suspended":
            logger.warning(f"User already suspended: {user_id}")
            return False
        
        result = self.db.update("users", user_id, {"status": "suspended"})
        if result:
            logger.info(f"User suspended: {user_id}")
        return result
    
    def reactivate_user(self, user_id: str) -> bool:
        """Reactivate a suspended client"""
        user = self.get_user(user_id)
        if user.get("status") == "active":
            logger.warning(f"User already active: {user_id}")
            return False
        
        result = self.db.update("users", user_id, {"status": "active"})
        if result:
            logger.info(f"User reactivated: {user_id}")
        return result
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        # Check if user has active bots
        bots = self.db.query("bots", {"owner_id": user_id, "status": "active"})
        if bots:
            raise ValidationException(
                f"Cannot delete user with {len(bots)} active bot(s)"
            )
        
        result = self.db.delete("users", user_id)
        if result:
            logger.info(f"User deleted: {user_id}")
        return result
    
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        user = self.get_user(user_id)
        
        # Count bots
        bots = self.db.query("bots", {"owner_id": user_id})
        
        # Count licenses
        licenses = self.db.query("licenses", {"user_id": user_id})
        
        # Calculate total spent
        transactions = self.db.query("transactions", {"user_id": user_id})
        total_spent = sum(t.get("amount", 0) for t in transactions if t.get("type") in ["bot_creation", "api_change"])
        
        return {
            "user_id": user_id,
            "telegram_id": user.get("telegram_id"),
            "username": user.get("username"),
            "balance": user.get("balance", 0.0),
            "status": user.get("status"),
            "bots_count": len(bots),
            "licenses_count": len(licenses),
            "api_changes": user.get("api_key_changes", 0),
            "total_spent": total_spent,
            "created_at": user.get("created_at"),
            "last_login": user.get("last_login"),
        }
