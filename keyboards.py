from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("📢 Create Promotion", callback_data="create_promo")],
        [InlineKeyboardButton("📜 View Commands", callback_data="view_commands")],
        [InlineKeyboardButton("👨‍💻 About Developer", callback_data="about_dev")],
        [InlineKeyboardButton("❓ Help", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_menu():
    """Admin menu keyboard"""
    keyboard = [
        [InlineKeyboardButton("👥 Manage Users", callback_data="manage_users")],
        [InlineKeyboardButton("⚙️ Group Settings", callback_data="group_settings")],
        [InlineKeyboardButton("📊 Statistics", callback_data="stats")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_promo_confirmation():
    """Promotion confirmation keyboard"""
    keyboard = [
        [InlineKeyboardButton("✅ Confirm & Send", callback_data="confirm_send")],
        [InlineKeyboardButton("✏️ Edit Text", callback_data="edit_text")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_promo")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_about_keyboard():
    """About developer keyboard"""
    keyboard = [
        [InlineKeyboardButton("🐦 X/Twitter", url="https://x.com/im_shoudo")],
        [InlineKeyboardButton("📚 GitHub", url="https://github.com/asikrshoudo")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)