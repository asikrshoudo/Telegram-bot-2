"""
Error handlers for the bot.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors in the bot."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Log the error
    error_msg = str(context.error)
    
    # Send error message to user if possible
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "An error occurred. Please try again later."
            )
        except:
            pass