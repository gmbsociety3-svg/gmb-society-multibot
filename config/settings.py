"""
Configuration Settings
Centralized configuration management for the entire system
"""

import os
from pathlib import Path
from enum import Enum
from typing import Optional

class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings:
    """Main settings class"""
    
    def __init__(self):
        # Environment
        self.environment = Environment(os.getenv("ENVIRONMENT", "development"))
        self.debug = self.environment == Environment.DEVELOPMENT
        
        # Telegram API
        self.bot_father_token = os.getenv("BOT_FATHER_TOKEN", "")
        self.owner_telegram_id = int(os.getenv("OWNER_TELEGRAM_ID", "0"))
        
        # Paths
        self.base_dir = Path(__file__).parent.parent.parent
        self.data_dir = self.base_dir / "data"
        self.logs_dir = self.base_dir / "logs"
        self.backups_dir = self.data_dir / "backups"
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        
        # Database
        self.use_json = os.getenv("USE_JSON", "true").lower() == "true"
        self.json_db_path = self.data_dir / "bot_father"
        self.json_db_path.mkdir(parents=True, exist_ok=True)
        
        # Bot hijo settings
        self.bot_hijo_dir = self.data_dir / "bot_hijo"
        self.bot_hijo_dir.mkdir(parents=True, exist_ok=True)
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # Plans (USD)
        self.PLANS = {
            30: 15.00,
            90: 40.00,
            365: 125.00
        }
        
        # API Change costs
        self.FIRST_API_CHANGE_COST = 0.00
        self.SUBSEQUENT_API_CHANGE_COST = 0.30
        
        # Timeouts
        self.API_VALIDATION_TIMEOUT = 10
        self.MESSAGE_TIMEOUT = 300  # 5 minutes
        
        # Backup settings
        self.AUTO_BACKUP_INTERVAL = 3600  # 1 hour
        self.BACKUP_RETENTION_DAYS = 30
        
        # Validation
        self.MAX_USERNAME_LENGTH = 50
        self.MAX_BOT_NAME_LENGTH = 100
        self.MIN_PASSWORD_LENGTH = 6
        
    def validate(self):
        """Validate critical settings"""
        if not self.bot_father_token:
            raise ValueError("BOT_FATHER_TOKEN not set in environment")
        if not self.owner_telegram_id:
            raise ValueError("OWNER_TELEGRAM_ID not set in environment")
        return True
