from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from database.database import db
from utils.helpers import escape_html

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new member joining"""
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            # Bot added to group
            await update.message.reply_text(
                "🤖 *Thanks for adding me!*\n\n"
                "Please make me admin to use all features.\n"
                "Use /help to see available commands.",
                parse_mode='Markdown'
            )
            # Add group to database
            db.add_group(
                group_id=update.effective_chat.id,
                group_name=update.effective_chat.title
            )
        else:
            # Regular user joined
            from database.database import db
            groups = db.get_all_groups()
            group_info = None
            for gid, gname in groups:
                if str(gid) == str(update.effective_chat.id):
                    group_info = (gid, gname)
                    break
            
            if group_info:
                welcome_msg = "👋 Welcome {user} to {group}!"
            else:
                welcome_msg = "👋 Welcome {user}!"
            
            # Format welcome message
            welcome_msg = welcome_msg.replace("{user}", member.mention_html())
            welcome_msg = welcome_msg.replace("{group}", escape_html(update.effective_chat.title))
            
            await update.message.reply_text(
                welcome_msg,
                parse_mode='HTML'
            )

async def goodbye_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle member leaving"""
    if update.message.left_chat_member:
        member = update.message.left_chat_member
        if member.id != context.bot.id:
            await update.message.reply_text(
                f"👋 Goodbye {member.mention_html()}! We'll miss you!",
                parse_mode='HTML'
            )

# Register handlers
def register_welcome_handlers(application):
    application.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS,
        welcome_new_member
    ))
    application.add_handler(MessageHandler(
        filters.StatusUpdate.LEFT_CHAT_MEMBER,
        goodbye_member
    ))