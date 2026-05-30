"""
Centralized Logging System
Structured logging with rotation and multiple handlers
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logging(
    name: str,
    log_level: str = "INFO",
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Setup logging with file and console handlers
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
    
    Returns:
        Configured logger instance
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level))
    
    if logger.hasHandlers():
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    if log_dir:
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
    
    return logger

class LogContext:
    """Context manager for structured logging"""
    
    def __init__(self, logger: logging.Logger, action: str, **context):
        self.logger = logger
        self.action = action
        self.context = context
    
    def __enter__(self):
        self.logger.info(f"Starting: {self.action} - Context: {self.context}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(
                f"Failed: {self.action} - Error: {exc_val}",
                exc_info=(exc_type, exc_val, exc_tb)
            )
            return False
        self.logger.info(f"Completed: {self.action}")
        return True
