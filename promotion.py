from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from utils.text_constants import ERROR_MESSAGES
from utils.keyboards import get_promo_confirmation
from database.database import db
import logging

logger = logging.getLogger(__name__)

# Store temporary promotion data
user_promotions = {}

async def promotion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /promotion command"""
    if update.effective_chat.type != "private":
        await update.message.reply_text(ERROR_MESSAGES["private_only"])
        return
    
    user_id = update.effective_user.id
    user_promotions[user_id] = {
        "text": "",
        "photo": None,
        "step": "waiting"
    }
    
    await update.message.reply_text(
        "📢 *Promotion System*\n\n"
        "Please send me the promotion content.\n"
        "You can send:\n"
        "• Text message\n"
        "• Text with links\n"
        "• Photo with caption\n"
        "• Any media with text\n\n"
        "I will share this in all groups I manage!\n\n"
        "Type /cancel to cancel.",
        parse_mode='Markdown'
    )

async def handle_promotion_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle promotion message from user"""
    if update.effective_chat.type != "private":
        return
    
    user_id = update.effective_user.id
    
    if user_id not in user_promotions:
        return
    
    promo_data = user_promotions[user_id]
    
    # Get text from message
    if update.message.text:
        promo_data["text"] = update.message.text
    elif update.message.caption:
        promo_data["text"] = update.message.caption
    
    # Get photo if available
    if update.message.photo:
        promo_data["photo"] = update.message.photo[-1].file_id
    
    # Show preview
    await show_promotion_preview(update, context, promo_data)

async def show_promotion_preview(update: Update, context: ContextTypes.DEFAULT_TYPE, promo_data):
    """Show promotion preview to user"""
    user_id = update.effective_user.id
    
    # Send preview
    if promo_data["photo"]:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=promo_data["photo"],
            caption=f"📋 *Preview:*\n\n{promo_data['text']}\n\n"
                    f"👉 This will be sent to all groups.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"📋 *Preview:*\n\n{promo_data['text']}\n\n"
            f"👉 This will be sent to all groups.",
            parse_mode='Markdown'
        )
    
    # Ask for confirmation
    await update.message.reply_text(
        "❓ *Confirm Promotion*\n\n"
        f"Text length: {len(promo_data['text'])} characters\n"
        f"Has photo: {'Yes' if promo_data['photo'] else 'No'}\n\n"
        "Do you want to send this promotion to all groups?",
        parse_mode='Markdown',
        reply_markup=get_promo_confirmation()
    )
    
    user_promotions[user_id]["step"] = "confirming"

async def send_promotion_to_all_groups(context, promo_data, user_id):
    """Send promotion to all groups"""
    groups = db.get_all_groups()
    sent_count = 0
    failed_count = 0
    
    if not groups:
        return 0, 0, "No groups found in database"
    
    for group_id, group_name in groups:
        try:
            if promo_data["photo"]:
                await context.bot.send_photo(
                    chat_id=group_id,
                    photo=promo_data["photo"],
                    caption=promo_data["text"],
                    parse_mode='Markdown' if promo_data["text"].startswith('*') else None
                )
            else:
                await context.bot.send_message(
                    chat_id=group_id,
                    text=promo_data["text"],
                    parse_mode='Markdown' if promo_data["text"].startswith('*') else None
                )
            sent_count += 1
        except Exception as e:
            logger.error(f"Failed to send to {group_name} ({group_id}): {e}")
            failed_count += 1
    
    # Save to database
    db.add_promotion(user_id, promo_data["text"], promo_data["photo"])
    
    return sent_count, failed_count, None

async def promotion_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle promotion confirmation buttons"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if user_id not in user_promotions:
        await query.edit_message_text("Promotion session expired. Please use /promotion again.")
        return
    
    if query.data == "confirm_send":
        await query.edit_message_text("📤 Sending promotion to all groups...")
        
        sent, failed, error = await send_promotion_to_all_groups(
            context, user_promotions[user_id], user_id
        )
        
        if error:
            await query.edit_message_text(f"❌ Error: {error}")
        else:
            await query.edit_message_text(
                f"✅ *Promotion Sent Successfully!*\n\n"
                f"✅ Sent to: {sent} groups\n"
                f"❌ Failed: {failed} groups\n\n"
                f"Thank you for using promotion system!",
                parse_mode='Markdown'
            )
        
        # Clean up
        if user_id in user_promotions:
            del user_promotions[user_id]
    
    elif query.data == "edit_text":
        await query.edit_message_text(
            "Please send the corrected promotion text:",
            reply_markup=None
        )
        user_promotions[user_id]["step"] = "editing"
    
    elif query.data == "cancel_promo":
        await query.edit_message_text("❌ Promotion cancelled.")
        if user_id in user_promotions:
            del user_promotions[user_id]

# Register handlers
def register_promotion_handlers(application):
    application.add_handler(CommandHandler("promotion", promotion_command))
    application.add_handler(MessageHandler(
        filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
        handle_promotion_message
    ))
    application.add_handler(MessageHandler(
        filters.PHOTO & filters.ChatType.PRIVATE,
        handle_promotion_message
    ))
    application.add_handler(CallbackQueryHandler(promotion_button_handler, pattern="^(confirm_send|edit_text|cancel_promo)$"))