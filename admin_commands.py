from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes, CommandHandler
from utils.helpers import is_admin, parse_time, format_time_delta
from utils.text_constants import ERROR_MESSAGES
import time
from database.database import db

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ban command"""
    if not await is_admin(update, context):
        await update.message.reply_text(ERROR_MESSAGES["no_admin"])
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(ERROR_MESSAGES["no_reply"])
        return
    
    user = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "No reason provided"
    
    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )
        await update.message.reply_text(
            f"✅ *User Banned*\n"
            f"👤 User: {user.mention_html()}\n"
            f"📛 Reason: {reason}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /kick command"""
    if not await is_admin(update, context):
        await update.message.reply_text(ERROR_MESSAGES["no_admin"])
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(ERROR_MESSAGES["no_reply"])
        return
    
    user = update.message.reply_to_message.from_user
    reason = " ".join(context.args) if context.args else "No reason provided"
    
    try:
        # Ban then unban to kick
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )
        await context.bot.unban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )
        await update.message.reply_text(
            f"✅ *User Kicked*\n"
            f"👤 User: {user.mention_html()}\n"
            f"📛 Reason: {reason}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mute command"""
    if not await is_admin(update, context):
        await update.message.reply_text(ERROR_MESSAGES["no_admin"])
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(ERROR_MESSAGES["no_reply"])
        return
    
    user = update.message.reply_to_message.from_user
    mute_time = "1h"  # Default
    
    if context.args:
        mute_time = context.args[0]
    
    try:
        mute_duration = parse_time(mute_time)
        until_date = int(time.time() + mute_duration.total_seconds())
        
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions=ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            ),
            until_date=until_date
        )
        
        await update.message.reply_text(
            f"✅ *User Muted*\n"
            f"👤 User: {user.mention_html()}\n"
            f"⏰ Duration: {format_time_delta(mute_duration)}",
            parse_mode='HTML'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /welcome command"""
    if not await is_admin(update, context):
        await update.message.reply_text(ERROR_MESSAGES["no_admin"])
        return
    
    welcome_text = " ".join(context.args)
    if not welcome_text:
        await update.message.reply_text(
            "Usage: `/welcome Your welcome message`\n\n"
            "Variables you can use:\n"
            "• `{user}` - User mention\n"
            "• `{group}` - Group name\n\n"
            "Example:\n"
            "`/welcome Hello {user}! Welcome to {group} group. Enjoy your stay!`",
            parse_mode='Markdown'
        )
        return
    
    db.update_welcome(update.effective_chat.id, welcome_text)
    await update.message.reply_text("✅ Welcome message updated!")

async def set_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rules command"""
    if not await is_admin(update, context):
        await update.message.reply_text(ERROR_MESSAGES["no_admin"])
        return
    
    rules_text = " ".join(context.args)
    if not rules_text:
        await update.message.reply_text(
            "Usage: `/rules Your group rules`\n\n"
            "Example:\n"
            "`/rules 1. No spam\\n2. Be respectful\\n3. No NSFW content`",
            parse_mode='Markdown'
        )
        return
    
    db.update_rules(update.effective_chat.id, rules_text)
    await update.message.reply_text("✅ Group rules updated!")

# Register handlers
def register_admin_handlers(application):
    application.add_handler(CommandHandler("ban", ban_user))
    application.add_handler(CommandHandler("kick", kick_user))
    application.add_handler(CommandHandler("mute", mute_user))
    application.add_handler(CommandHandler("welcome", set_welcome))
    application.add_handler(CommandHandler("rules", set_rules))