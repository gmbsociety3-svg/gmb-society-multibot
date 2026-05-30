"""
Input Validators
Comprehensive validation for all user inputs
"""

import re
from typing import Optional, Tuple
from src.utils.exceptions import ValidationException

class Validators:
    """Collection of validation functions"""
    
    # Regex patterns
    BOT_TOKEN_PATTERN = re.compile(r'^\d+:[\w_\-]{27}$')
    TELEGRAM_ID_PATTERN = re.compile(r'^\d{6,}$')
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_]{3,50}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    @staticmethod
    def validate_bot_token(token: str) -> Tuple[bool, str]:
        """
        Validate Telegram bot token format
        
        Args:
            token: Bot token to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        token = token.strip()
        
        if not token:
            return False, "Token cannot be empty"
        
        if len(token) < 20:
            return False, "Token format invalid (too short)"
        
        if not Validators.BOT_TOKEN_PATTERN.match(token):
            return False, "Token format invalid. Expected: digits:alphanumeric"
        
        return True, ""
    
    @staticmethod
    def validate_telegram_id(telegram_id: int) -> Tuple[bool, str]:
        """Validate Telegram ID format"""
        if not isinstance(telegram_id, int):
            return False, "Telegram ID must be an integer"
        
        if telegram_id < 100000000:
            return False, "Invalid Telegram ID"
        
        return True, ""
    
    @staticmethod
    def validate_username(username: str, min_length: int = 3, max_length: int = 50) -> Tuple[bool, str]:
        """
        Validate username format
        
        Args:
            username: Username to validate
            min_length: Minimum username length
            max_length: Maximum username length
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        username = username.strip()
        
        if not username:
            return False, "Username cannot be empty"
        
        if len(username) < min_length or len(username) > max_length:
            return False, f"Username must be between {min_length} and {max_length} characters"
        
        if not Validators.USERNAME_PATTERN.match(username):
            return False, "Username can only contain letters, numbers and underscores"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> Tuple[bool, str]:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            min_length: Minimum password length
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < min_length:
            return False, f"Password must be at least {min_length} characters"
        
        if len(password) > 255:
            return False, "Password is too long"
        
        return True, ""
    
    @staticmethod
    def validate_amount(amount: float, min_amount: float = 0.01) -> Tuple[bool, str]:
        """Validate monetary amount"""
        if not isinstance(amount, (int, float)):
            return False, "Amount must be a number"
        
        if amount < min_amount:
            return False, f"Amount must be at least ${min_amount}"
        
        if amount > 999999.99:
            return False, "Amount exceeds maximum limit"
        
        return True, ""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(url):
            return False, "Invalid URL format"
        
        return True, ""
    
    @staticmethod
    def validate_bot_name(name: str, max_length: int = 100) -> Tuple[bool, str]:
        """Validate bot name"""
        name = name.strip()
        
        if not name:
            return False, "Bot name cannot be empty"
        
        if len(name) > max_length:
            return False, f"Bot name cannot exceed {max_length} characters"
        
        if len(name) < 3:
            return False, "Bot name must be at least 3 characters"
        
        return True, ""
    
    @staticmethod
    def validate_product_name(name: str) -> Tuple[bool, str]:
        """Validate product name"""
        name = name.strip()
        
        if not name:
            return False, "Product name cannot be empty"
        
        if len(name) < 2:
            return False, "Product name too short"
        
        if len(name) > 100:
            return False, "Product name too long"
        
        return True, ""
    
    @staticmethod
    def validate_duration_days(days: int) -> Tuple[bool, str]:
        """Validate duration in days"""
        if not isinstance(days, int):
            return False, "Duration must be an integer"
        
        if days < 1 or days > 365:
            return False, "Duration must be between 1 and 365 days"
        
        return True, ""
    
    @staticmethod
    def validate_price(price: float) -> Tuple[bool, str]:
        """Validate product price"""
        if price < 0.01:
            return False, "Price must be at least $0.01"
        
        if price > 99999.99:
            return False, "Price exceeds maximum limit"
        
        return True, ""

    @staticmethod
    def validate_text_field(text: str, field_name: str = "Field", 
                           min_length: int = 1, max_length: int = 5000) -> Tuple[bool, str]:
        """Generic text field validation"""
        if not text:
            return False, f"{field_name} cannot be empty"
        
        if len(text) < min_length:
            return False, f"{field_name} too short (minimum {min_length} characters)"
        
        if len(text) > max_length:
            return False, f"{field_name} too long (maximum {max_length} characters)"
        
        return True, ""
