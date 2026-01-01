"""
User command handlers.
"""

from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes

# Handler functions
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text("Hello! I'm your bot. 👋")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/about - About this bot
"""
    await update.message.reply_text(help_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command."""
    await update.message.reply_text("This is a Telegram bot built with python-telegram-bot.")

# List of handlers
handlers = [
    CommandHandler("start", start_command),
    CommandHandler("help", help_command),
    CommandHandler("about", about_command),
]