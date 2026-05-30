"""
GMB SOCIETY MULTIBOT SYSTEM
Professional Architecture - Main Entry Point

System: Bot Father + Bot Hijo
Version: 1.0.0
Author: GMB Society
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.settings import Settings
from src.bot_father.core.bot import BotFatherManager
from src.utils.logger import setup_logging

# Initialize logging
logger = setup_logging("GMB_MULTIBOT_SYSTEM")

def main():
    """Main entry point for GMB Society Multibot System"""
    try:
        logger.info("=" * 60)
        logger.info("GMB SOCIETY MULTIBOT SYSTEM - STARTING")
        logger.info("=" * 60)
        
        # Load configuration
        settings = Settings()
        logger.info(f"Configuration loaded: {settings.environment}")
        
        # Initialize Bot Father
        bot_father = BotFatherManager(settings)
        logger.info("Bot Father initialized successfully")
        
        # Start Bot Father
        bot_father.run()
        
    except Exception as e:
        logger.critical(f"Critical error in main: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
