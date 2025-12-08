import html
import logging
from datetime import datetime, timedelta
from telegram import ChatPermissions
from config import Config

logger = logging.getLogger(__name__)

def escape_html(text):
    """Escape HTML special characters"""
    return html.escape(str(text))

async def is_admin(update, context, user_id=None):
    """Check if user is admin in group"""
    if update.effective_chat.type == "private":
        return False
    
    if user_id is None:
        user_id = update.effective_user.id
    
    try:
        member = await context.bot.get_chat_member(update.effective_chat.id, user_id)
        return member.status in ['administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking admin: {e}")
        return False

async def is_bot_admin(context, chat_id):
    """Check if bot is admin in group"""
    try:
        bot_id = context.bot.id
        member = await context.bot.get_chat_member(chat_id, bot_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def parse_time(time_str):
    """Parse time string like 1h, 30m, 2d"""
    time_str = time_str.lower().strip()
    
    if not time_str:
        return timedelta(hours=1)  # Default
    
    if time_str.endswith('m'):
        minutes = int(time_str[:-1])
        return timedelta(minutes=minutes)
    elif time_str.endswith('h'):
        hours = int(time_str[:-1])
        return timedelta(hours=hours)
    elif time_str.endswith('d'):
        days = int(time_str[:-1])
        return timedelta(days=days)
    elif time_str.endswith('s'):
        seconds = int(time_str[:-1])
        return timedelta(seconds=seconds)
    else:
        # Try to parse as minutes
        try:
            minutes = int(time_str)
            return timedelta(minutes=minutes)
        except:
            return timedelta(hours=1)

def format_time_delta(delta):
    """Format timedelta to readable string"""
    total_seconds = int(delta.total_seconds())
    
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds and not (days or hours or minutes):
        parts.append(f"{seconds}s")
    
    return " ".join(parts) if parts else "0s"