"""
Handlers package for Telegram bot commands.
"""

from telegram.ext import Application


def register_handlers(application: Application):
    """Register all handlers with the application."""
    # Import handlers here
    from . import user_handlers
    from . import admin_handlers
    from . import error_handlers
    
    # Register handler groups
    application.add_handlers(user_handlers.handlers)
    application.add_handlers(admin_handlers.handlers)
    application.add_error_handler(error_handlers.error_handler)
    
    # Log registration
    import logging
    logger = logging.getLogger(__name__)
    logger.info("All handlers registered")