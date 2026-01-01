#!/usr/bin/env python3
"""
Main entry point for the Telegram bot.
"""

import logging
import asyncio
from telegram.ext import Application, ApplicationBuilder

from config.settings import BOT_TOKEN, LOG_LEVEL, LOG_FILE
from src.handlers import register_handlers
from src.services.database import init_database


def setup_logging():
    """Configure logging for the bot."""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    # Create logs directory if it doesn't exist
    import os
    os.makedirs("logs", exist_ok=True)
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)


async def main():
    """Start the bot."""
    logger = setup_logging()
    
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set in environment variables!")
        return
    
    try:
        # Initialize database
        await init_database()
        logger.info("Database initialized")
        
        # Build the application
        application = ApplicationBuilder() \
            .token(BOT_TOKEN) \
            .concurrent_updates(True) \
            .build()
        
        # Register all handlers
        register_handlers(application)
        logger.info("Handlers registered")
        
        # Start the bot
        logger.info("Starting bot...")
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        # Keep the bot running
        await asyncio.Event().wait()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
    finally:
        if 'application' in locals():
            await application.stop()


if __name__ == '__main__':
    asyncio.run(main())