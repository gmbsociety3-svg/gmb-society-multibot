"""
Balance Management Service
Handle balance operations and transactions
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from src.database.db_manager import DatabaseManager
from src.utils.exceptions import InsufficientBalanceException, ValidationException
from src.utils.validators import Validators

logger = logging.getLogger(__name__)

class BalanceService:
    """Manage user balance operations"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
    
    def get_balance(self, user_id: str) -> float:
        """Get current user balance"""
        user = self.db.read("users", user_id)
        if not user:
            raise ValidationException(f"User not found: {user_id}")
        return user.get("balance", 0.0)
    
    def add_balance(self, user_id: str, amount: float, description: str = "") -> bool:
        """
        Add balance to user account
        
        Args:
            user_id: User ID
            amount: Amount to add
            description: Transaction description
        
        Returns:
            True if successful
        
        Raises:
            ValidationException: If amount invalid
        """
        is_valid, error = Validators.validate_amount(amount)
        if not is_valid:
            raise ValidationException(error)
        
        user = self.db.read("users", user_id)
        if not user:
            raise ValidationException(f"User not found: {user_id}")
        
        old_balance = user.get("balance", 0.0)
        new_balance = old_balance + amount
        
        # Update balance
        self.db.update("users", user_id, {"balance": new_balance})
        
        # Record transaction
        self._record_transaction(
            user_id,
            "add_balance",
            amount,
            old_balance,
            new_balance,
            description or "Balance added by owner"
        )
        
        logger.info(f"Balance added: {user_id} +${amount} (new: ${new_balance})")
        return True
    
    def deduct_balance(self, user_id: str, amount: float, 
                       transaction_type: str, description: str = "") -> bool:
        """
        Deduct balance from user account
        
        Args:
            user_id: User ID
            amount: Amount to deduct
            transaction_type: Type of transaction
            description: Transaction description
        
        Returns:
            True if successful
        
        Raises:
            InsufficientBalanceException: If insufficient balance
            ValidationException: If amount invalid
        """
        is_valid, error = Validators.validate_amount(amount)
        if not is_valid:
            raise ValidationException(error)
        
        user = self.db.read("users", user_id)
        if not user:
            raise ValidationException(f"User not found: {user_id}")
        
        old_balance = user.get("balance", 0.0)
        
        if old_balance < amount:
            raise InsufficientBalanceException(
                f"Insufficient balance. Available: ${old_balance}, Required: ${amount}"
            )
        
        new_balance = old_balance - amount
        
        # Update balance
        self.db.update("users", user_id, {"balance": new_balance})
        
        # Record transaction
        self._record_transaction(
            user_id,
            transaction_type,
            amount,
            old_balance,
            new_balance,
            description
        )
        
        logger.info(f"Balance deducted: {user_id} -${amount} (new: ${new_balance})")
        return True
    
    def _record_transaction(self, user_id: str, transaction_type: str, 
                           amount: float, balance_before: float, 
                           balance_after: float, description: str) -> str:
        """
        Record a transaction in the ledger
        
        Returns:
            Transaction ID
        """
        transaction = {
            "user_id": user_id,
            "type": transaction_type,
            "amount": amount,
            "balance_before": balance_before,
            "balance_after": balance_after,
            "description": description,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        transaction_id = self.db.create("transactions", transaction)
        return transaction_id
    
    def get_user_transactions(self, user_id: str, limit: int = 50) -> list:
        """Get user transaction history"""
        transactions = self.db.query("transactions", {"user_id": user_id})
        # Sort by timestamp descending
        transactions.sort(key=lambda t: t.get("timestamp", ""), reverse=True)
        return transactions[:limit]
    
    def get_balance_summary(self) -> Dict[str, Any]:
        """Get system balance summary"""
        all_users = self.db.list_all("users")
        clients = [u for u in all_users if u.get("role") == "client"]
        
        total_balance = sum(u.get("balance", 0.0) for u in clients)
        total_users = len(clients)
        
        return {
            "total_users": total_users,
            "total_balance": total_balance,
            "average_balance": total_balance / total_users if total_users > 0 else 0,
            "highest_balance": max((u.get("balance", 0) for u in clients), default=0),
            "lowest_balance": min((u.get("balance", 0) for u in clients), default=0),
        }
