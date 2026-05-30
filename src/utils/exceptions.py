"""
Custom Exceptions for GMB Society Multibot System
"""

class GMBException(Exception):
    """Base exception for all GMB exceptions"""
    pass

class AuthenticationException(GMBException):
    """Raised when authentication fails"""
    pass

class AuthorizationException(GMBException):
    """Raised when user lacks permissions"""
    pass

class UserNotFoundException(GMBException):
    """Raised when user is not found"""
    pass

class InsufficientBalanceException(GMBException):
    """Raised when user has insufficient balance"""
    pass

class InvalidTokenException(GMBException):
    """Raised when bot token is invalid"""
    pass

class BotCreationException(GMBException):
    """Raised when bot creation fails"""
    pass

class LicenseException(GMBException):
    """Raised when license operation fails"""
    pass

class LicenseExpiredException(GMBException):
    """Raised when license has expired"""
    pass

class ProductNotFoundException(GMBException):
    """Raised when product is not found"""
    pass

class InsufficientKeyException(GMBException):
    """Raised when no keys available"""
    pass

class PurchaseException(GMBException):
    """Raised when purchase operation fails"""
    pass

class DatabaseException(GMBException):
    """Raised when database operation fails"""
    pass

class ValidationException(GMBException):
    """Raised when validation fails"""
    pass

class ConfigurationException(GMBException):
    """Raised when configuration is invalid"""
    pass
