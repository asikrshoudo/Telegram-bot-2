from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.text_constants import START_MESSAGE, HELP_MESSAGE, ABOUT_MESSAGE
from utils.keyboards import get_main_menu, get_about_keyboard

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    username = user.username or user.first_name
    
    message = START_MESSAGE.format(username=username)
    
    await update.message.reply_text(
        message,
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    await update.message.reply_text(
        ABOUT_MESSAGE,
        parse_mode='Markdown',
        reply_markup=get_about_keyboard(),
        disable_web_page_preview=False
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /id command"""
    user = update.effective_user
    chat = update.effective_chat
    
    text = f"👤 *Your ID:* `{user.id}`\n"
    text += f"📛 *Name:* {user.first_name}\n"
    
    if user.username:
        text += f"🔗 *Username:* @{user.username}\n"
    
    if chat.type != "private":
        text += f"\n💬 *Chat ID:* `{chat.id}`\n"
        text += f"🏷️ *Chat Title:* {chat.title}\n"
        text += f"📝 *Chat Type:* {chat.type}"
    
    await update.message.reply_text(text, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button clicks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "main_menu":
        await query.edit_message_text(
            START_MESSAGE.format(username=query.from_user.first_name),
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
    
    elif query.data == "view_commands":
        await query.edit_message_text(
            HELP_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
    
    elif query.data == "about_dev":
        await query.edit_message_text(
            ABOUT_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_about_keyboard(),
            disable_web_page_preview=False
        )
    
    elif query.data == "help":
        await query.edit_message_text(
            HELP_MESSAGE,
            parse_mode='Markdown',
            reply_markup=get_main_menu()
        )
    
    elif query.data == "create_promo":
        await query.edit_message_text(
            "📢 *Promotion Creator*\n\n"
            "Please send me your promotion message.\n"
            "You can include text, links, and photos!\n\n"
            "Type /cancel to cancel.",
            parse_mode='Markdown'
        )
        context.user_data['creating_promo'] = True

# Register handlers
def register_user_handlers(application):
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("id", id_command))