"""
Admin command handlers.
"""

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from config.settings import ADMIN_IDS

# Check if user is admin
def is_admin(user_id: int) -> bool:
    """Check if user is admin."""
    return user_id in ADMIN_IDS

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command."""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    
    await update.message.reply_text("Welcome to admin panel!")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command."""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("You are not authorized to use this command.")
        return
    
    stats_text = "Bot Statistics:\n- Users: 0\n- Groups: 0\n- Messages: 0"
    await update.message.reply_text(stats_text)

# List of handlers
handlers = [
    CommandHandler("admin", admin_command),
    CommandHandler("stats", stats_command),
]