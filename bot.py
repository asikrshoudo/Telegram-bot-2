#!/usr/bin/env python3
"""
Universal Telegram Group Management Bot
Anyone can use - No restrictions!
Developer: www.x.com/im_shoudo
"""

import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# সরাসরি আপনার টোকেন
TOKEN = "8353713232:AAH9c3MLO5z-o3HRDbHOzs453ysfMFrKFkQ"

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# ডাটাবেস ক্লাস
class Database:
    def __init__(self, db_path="database/groups.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_tables()
    
    def init_tables(self):
        """ডাটাবেস টেবিল তৈরি করুন"""
        # গ্রুপ টেবিল
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id TEXT UNIQUE,
                group_name TEXT,
                welcome_msg TEXT,
                rules_msg TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # প্রোমোশন টেবিল
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                message TEXT,
                photo_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        logger.info("✅ Database initialized successfully")
    
    def add_group(self, group_id, group_name):
        """নতুন গ্রুপ যোগ করুন"""
        try:
            self.cursor.execute(
                "INSERT OR IGNORE INTO groups (group_id, group_name) VALUES (?, ?)",
                (str(group_id), group_name)
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Error adding group: {e}")
            return False
    
    def update_rules(self, group_id, rules_msg):
        """গ্রুপের রুলস আপডেট করুন"""
        try:
            self.cursor.execute(
                "UPDATE groups SET rules_msg = ? WHERE group_id = ?",
                (rules_msg, str(group_id))
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Error updating rules: {e}")
            return False
    
    def get_rules(self, group_id):
        """গ্রুপের রুলস পান"""
        self.cursor.execute(
            "SELECT rules_msg FROM groups WHERE group_id = ?",
            (str(group_id),)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def update_welcome(self, group_id, welcome_msg):
        """গ্রুপের ওয়েলকাম মেসেজ আপডেট করুন"""
        try:
            self.cursor.execute(
                "UPDATE groups SET welcome_msg = ? WHERE group_id = ?",
                (welcome_msg, str(group_id))
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"❌ Error updating welcome: {e}")
            return False
    
    def get_welcome(self, group_id):
        """গ্রুপের ওয়েলকাম মেসেজ পান"""
        self.cursor.execute(
            "SELECT welcome_msg FROM groups WHERE group_id = ?",
            (str(group_id),)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def add_promotion(self, user_id, user_name, message, photo_id=None):
        """প্রোমোশন যোগ করুন"""
        try:
            self.cursor.execute(
                """INSERT INTO promotions (user_id, user_name, message, photo_id) 
                   VALUES (?, ?, ?, ?)""",
                (user_id, user_name, message, photo_id)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            logger.error(f"❌ Error adding promotion: {e}")
            return None
    
    def get_all_groups(self):
        """সকল গ্রুপ পান"""
        self.cursor.execute("SELECT group_id, group_name FROM groups")
        return self.cursor.fetchall()
# গ্লোবাল ডাটাবেস ইনস্ট্যান্স
db = Database()

# টেম্পোরারি স্টোরেজ
user_states = {}

# ==================== HELPER FUNCTIONS ====================

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """চেক করুন ইউজার গ্রুপে অ্যাডমিন কিনা"""
    if update.effective_chat.type == "private":
        return False
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

async def is_bot_admin(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    """চেক করুন বট অ্যাডমিন কিনা"""
    try:
        bot_id = context.bot.id
        member = await context.bot.get_chat_member(chat_id, bot_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def format_rules_display(rules_text):
    """রুলস ডিসপ্লে ফরম্যাট করুন"""
    lines = rules_text.split('\n')
    formatted = "📜 *Group Rules:*\n\n"
    
    for i, line in enumerate(lines, 1):
        if line.strip():
            formatted += f"{i}. {line.strip()}\n"
    
    return formatted
# ==================== START & HELP COMMANDS ====================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /start কমান্ড"""
    user = update.effective_user
    username = user.first_name
    
    welcome_text = f"""Hi {username}! How can I assist you today?

I can manage your groups or channels.
Also I can promote any of your links, posts, or images!!

*🔧 Features:*
• Group Management (ban/kick/mute)
• Set Welcome Messages
• Upload Group Rules 📜
• Promotion System 📢
• Multi-group Support

*👮 Admin Commands (in groups):*
/ban - Ban a user
/kick - Kick a user  
/mute - Mute a user
/welcome - Set welcome message
/rules - Set/view group rules
/uploadrules - Upload rules from text

*👤 User Commands:*
/start - Start the bot
/help - Show help
/id - Get your ID
/stats - Bot statistics
/about - About developer

*📢 Promotion Feature:*
Send /promotion in private chat!
"""
    
    keyboard = [
        [InlineKeyboardButton("📜 How to Use", callback_data="how_to_use")],
        [InlineKeyboardButton("📢 Create Promotion", callback_data="create_promo")],
        [InlineKeyboardButton("👨‍💻 About Developer", callback_data="about_dev")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /help কমান্ড"""
    help_text = """*🆘 Help Guide - Everyone Can Use!*

*For Everyone:*
• Add me to any group
• Make me admin (optional for some features)
• Use commands freely!

*📜 Rules Upload System:*
1. In your group, type: `/uploadrules`
2. Send your rules as text (each rule on new line)
3. Rules will be saved automatically
4. Anyone can view with `/rules`

*📢 Promotion System:*
1. Message me privately
2. Type `/promotion`
3. Send your promotion text/photo
4. I'll share in all my groups!

*👮 Group Management:*
• /ban [reply] - Ban user (admin only)
• /kick [reply] - Kick user (admin only)
• /mute [reply] - Mute user (admin only)
• /welcome [text] - Set welcome (admin only)
• /rules - View rules (everyone)

*📞 Contact Developer:* www.x.com/im_shoudo
"""
    
    keyboard = [
        [InlineKeyboardButton("📜 Upload Rules Guide", callback_data="rules_guide")],
        [InlineKeyboardButton("📢 Promotion Guide", callback_data="promo_guide")],
        [InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /about কমান্ড"""
    about_text = """*👨‍💻 About This Bot*

*Developer:* Shoudo
*Twitter/X:* [www.x.com/im_shoudo](https://www.x.com/im_shoudo)

*🌟 Bot Features:*
• ✅ **Everyone can use** - No restrictions!
• ✅ **Rules Upload System** - Upload rules easily
• ✅ **Promotion System** - Share in multiple groups
• ✅ **Group Management** - Ban, Kick, Mute users
• ✅ **Welcome Messages** - Customizable welcomes

*🔧 Technology:*
• Built with Python 3
• Using python-telegram-bot library
• SQLite database for storage
• Open for all users

*🤝 Support:*
For any issues or suggestions, contact:
www.x.com/im_shoudo
"""
    
    keyboard = [
        [InlineKeyboardButton("🐦 Follow on X", url="https://www.x.com/im_shoudo")],
        [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        about_text, 
        parse_mode='Markdown', 
        reply_markup=reply_markup,
        disable_web_page_preview=False
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /id কমান্ড"""
    user = update.effective_user
    chat = update.effective_chat
    
    text = f"*👤 Your Information:*\n\n"
    text += f"• *User ID:* `{user.id}`\n"
    text += f"• *Name:* {user.first_name}\n"
    
    if user.last_name:
        text += f"• *Last Name:* {user.last_name}\n"
    
    if user.username:
        text += f"• *Username:* @{user.username}\n"
    
    text += f"\n*💬 Chat Info:*\n"
    text += f"• *Chat ID:* `{chat.id}`\n"
    text += f"• *Chat Type:* {chat.type}\n"
    
    if chat.type != "private":
        text += f"• *Chat Title:* {chat.title}\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')
# ==================== RULES SYSTEM (UPLOAD & VIEW) ====================

async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /rules কমান্ড - রুলস দেখান"""
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "📜 *Rules Command*\n\n"
            "This command works in groups only!\n"
            "Add me to your group and use `/rules` to view group rules.",
            parse_mode='Markdown'
        )
        return
    
    group_id = update.effective_chat.id
    rules_text = db.get_rules(group_id)
    
    if rules_text:
        formatted_rules = format_rules_display(rules_text)
        await update.message.reply_text(formatted_rules, parse_mode='Markdown')
    else:
        keyboard = [
            [InlineKeyboardButton("📝 Set Rules Now", callback_data="set_rules_now")],
            [InlineKeyboardButton("❓ How to Set Rules", callback_data="rules_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "*📜 No Rules Set Yet!*\n\n"
            "This group doesn't have any rules set up yet.\n\n"
            "*To set rules:*\n"
            "1. Use `/uploadrules` command\n"
            "2. Or use `/rules Your rules here`\n\n"
            "*Note:* You need to be admin to set rules.",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

async def uploadrules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /uploadrules কমান্ড - রুলস আপলোড শুরু করুন"""
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ This command only works in groups!\n"
            "Add me to your group and make me admin to upload rules."
        )
        return
    
    # চেক করুন ইউজার অ্যাডমিন কিনা
    if not await is_admin(update, context):
        await update.message.reply_text(
            "❌ You need to be admin to upload rules!\n\n"
            "Please ask a group admin to set the rules."
        )
        return
    
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # ইউজার স্টেট সেট করুন
    user_states[user_id] = {
        'action': 'uploading_rules',
        'chat_id': chat_id,
        'step': 'waiting_rules'
    }
    
    await update.message.reply_text(
        "*📝 Rules Upload System*\n\n"
        "Please send me the group rules.\n\n"
        "*Format:*\n"
        "• Each rule on a new line\n"
        "• Use numbers or bullet points\n"
        "• Keep it clear and concise\n\n"
        "*Example:*\n"
        "1. No spam or advertising\n"
        "2. Be respectful to everyone\n"
        "3. No NSFW content\n"
        "4. Follow Telegram's ToS\n\n"
        "Send your rules now or type /cancel to cancel.",
        parse_mode='Markdown'
    )

async def setrules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /rules with text - সরাসরি রুলস সেট করুন"""
    if update.effective_chat.type == "private":
        await update.message.reply_text(
            "❌ This command only works in groups!"
        )
        return
    
    # চেক করুন ইউজার অ্যাডমিন কিনা
    if not await is_admin(update, context):
        await update.message.reply_text(
            "❌ You need to be admin to set rules!"
        )
        return
    
    rules_text = " ".join(context.args)
    if not rules_text:
        await update.message.reply_text(
            "*Usage:* `/rules Your rules here`\n\n"
            "*Example:*\n"
            "`/rules 1. No spam\\n2. Be respectful\\n3. Have fun!`",
            parse_mode='Markdown'
        )
        return
    
    # রুলস সেভ করুন
    if db.update_rules(update.effective_chat.id, rules_text):
        await update.message.reply_text(
            "✅ *Rules Updated Successfully!*\n\n"
            "Use `/rules` to view the rules.\n"
            "New members will see these rules.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("❌ Failed to save rules. Please try again.")

async def handle_rules_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """রুলস টেক্সট গ্রহণ করুন"""
    user_id = update.effective_user.id
    
    if user_id not in user_states:
        return
    
    if user_states[user_id].get('action') != 'uploading_rules':
        return
    
    if user_states[user_id].get('step') != 'waiting_rules':
        return
    
    rules_text = update.message.text
    chat_id = user_states[user_id]['chat_id']
    
    # রুলস সেভ করুন
    if db.update_rules(chat_id, rules_text):
        # গ্রুপে কনফার্মেশন পাঠান
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"✅ *Rules Uploaded Successfully!*\n\n"
                     f"Rules have been set for this group.\n"
                     f"Use `/rules` to view them anytime.",
                parse_mode='Markdown'
            )
        except:
            pass
        
        # ইউজারকে কনফার্মেশন পাঠান
        await update.message.reply_text(
            "✅ *Rules Uploaded Successfully!*\n\n"
            f"Rules have been saved for the group.\n"
            f"Members can view them using `/rules` command.",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            "❌ Failed to save rules. Please try again with /uploadrules"
        )
    
    # ইউজার স্টেট ক্লিয়ার করুন
    if user_id in user_states:
        del user_states[user_id]
# ==================== GROUP MANAGEMENT COMMANDS ====================

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /ban কমান্ড"""
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ This command only works in groups!")
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("❌ You need to be admin to ban users!")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a user's message to ban!")
        return
    
    user = update.message.reply_to_message.from_user
    
    try:
        await context.bot.ban_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id
        )
        await update.message.reply_text(f"✅ User @{user.username or user.first_name} has been banned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /kick কমান্ড"""
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ This command only works in groups!")
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("❌ You need to be admin to kick users!")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a user's message to kick!")
        return
    
    user = update.message.reply_to_message.from_user
    
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
        await update.message.reply_text(f"✅ User @{user.username or user.first_name} has been kicked!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /mute কমান্ড"""
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ This command only works in groups!")
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("❌ You need to be admin to mute users!")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text("❌ Please reply to a user's message to mute!")
        return
    
    user = update.message.reply_to_message.from_user
    
    try:
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=user.id,
            permissions={
                'can_send_messages': False,
                'can_send_media_messages': False,
                'can_send_polls': False,
                'can_send_other_messages': False,
                'can_add_web_page_previews': False,
                'can_change_info': False,
                'can_invite_users': False,
                'can_pin_messages': False
            }
        )
        await update.message.reply_text(f"✅ User @{user.username or user.first_name} has been muted!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /welcome কমান্ড"""
    if update.effective_chat.type == "private":
        await update.message.reply_text("❌ This command only works in groups!")
        return
    
    if not await is_admin(update, context):
        await update.message.reply_text("❌ You need to be admin to set welcome message!")
        return
    
    welcome_text = " ".join(context.args)
    if welcome_text:
        # সেভ করুন ডাটাবেসে
        if db.update_welcome(update.effective_chat.id, welcome_text):
            await update.message.reply_text(f"✅ Welcome message set to:\n\n{welcome_text}")
        else:
            await update.message.reply_text("❌ Failed to save welcome message.")
    else:
        await update.message.reply_text(
            "*Usage:* `/welcome Your welcome message`\n\n"
            "*Example:*\n"
            "`/welcome Hello {user}! Welcome to {group} group.`",
            parse_mode='Markdown'
        )
# ==================== PROMOTION SYSTEM ====================

async def promotion_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /promotion কমান্ড"""
    if update.effective_chat.type != "private":
        await update.message.reply_text(
            "❌ Promotion feature only works in private chat!\n"
            "👉 Please message me privately and use /promotion"
        )
        return
    
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # ইউজার স্টেট সেট করুন
    user_states[user_id] = {
        'action': 'creating_promotion',
        'step': 'waiting_text',
        'user_name': user_name
    }
    
    await update.message.reply_text(
        "📢 *Promotion Creator*\n\n"
        "Send me the promotion text (with links if needed).\n\n"
        "*Examples:*\n"
        "• Join our group: https://t.me/example\n"
        "• Check out our website: https://example.com\n"
        "• New product launch! Buy now!\n\n"
        "You can also send a photo with caption.\n\n"
        "Type /cancel to cancel.",
        parse_mode='Markdown'
    )

async def handle_promotion_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """প্রোমোশন টেক্সট গ্রহণ করুন"""
    if update.effective_chat.type != "private":
        return
    
    user_id = update.effective_user.id
    
    if user_id not in user_states:
        return
    
    if user_states[user_id].get('action') != 'creating_promotion':
        return
    
    if user_states[user_id].get('step') != 'waiting_text':
        return
    
    promo_text = update.message.text
    user_states[user_id]['text'] = promo_text
    user_states[user_id]['step'] = 'waiting_photo_or_confirm'
    
    # প্রিভিউ দেখান
    keyboard = [
        [InlineKeyboardButton("✅ Send Without Photo", callback_data="send_no_photo")],
        [InlineKeyboardButton("📸 Add Photo", callback_data="add_photo")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_promo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"📋 *Promotion Preview:*\n\n{promo_text}\n\n"
        f"*Next:* Add a photo or send without photo?",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

async def handle_promotion_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """প্রোমোশন ফটো গ্রহণ করুন"""
    if update.effective_chat.type != "private":
        return
    
    user_id = update.effective_user.id
    
    if user_id not in user_states:
        return
    
    if user_states[user_id].get('action') != 'creating_promotion':
        return
    
    if user_states[user_id].get('step') != 'waiting_photo_or_confirm':
        return
    
    if update.message.photo:
        photo_id = update.message.photo[-1].file_id
        user_states[user_id]['photo_id'] = photo_id
        
        # ক্যাপশন থাকলে ব্যবহার করুন
        if update.message.caption:
            user_states[user_id]['text'] = update.message.caption
    
    # কনফার্মেশন দেখান
    keyboard = [
        [InlineKeyboardButton("✅ Confirm & Send", callback_data="confirm_send")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_promo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if 'photo_id' in user_states[user_id]:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=user_states[user_id]['photo_id'],
            caption=f"📋 *Promotion Preview:*\n\n{user_states[user_id]['text']}",
            parse_mode='Markdown'
        )
    
    await update.message.reply_text(
        "❓ *Confirm Promotion*\n\n"
        "Do you want to send this promotion to all groups?",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )
# ==================== BUTTON HANDLER ====================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল ইনলাইন বাটন ক্লিক"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "main_menu":
        await start_command(update, context)
    
    elif data == "how_to_use":
        await query.edit_message_text(
            "*📖 How to Use This Bot*\n\n"
            "1. *Add to Group:* Add me to any Telegram group\n"
            "2. *Make Admin:* For full features, make me admin\n"
            "3. *Set Rules:* Use /uploadrules to upload group rules\n"
            "4. *Promotions:* Message me privately for promotions\n"
            "5. *Manage:* Use /ban, /kick, /mute to manage users\n\n"
            "*Everyone can use all features!*",
            parse_mode='Markdown'
        )
    
    elif data == "create_promo":
        await query.edit_message_text(
            "📢 *Promotion System*\n\n"
            "To create a promotion:\n"
            "1. Message me privately\n"
            "2. Type /promotion\n"
            "3. Send your promotion text\n"
            "4. Add photo (optional)\n"
            "5. I'll share in all groups!\n\n"
            "👉 Go to private chat now!",
            parse_mode='Markdown'
        )
    
    elif data == "about_dev":
        await about_command(update, context)
    
    elif data == "rules_guide":
        await query.edit_message_text(
            "*📜 Rules Upload Guide*\n\n"
            "*Step-by-Step:*\n"
            "1. Add me to your group\n"
            "2. Make me admin (optional)\n"
            "3. Type /uploadrules\n"
            "4. Send your rules as text\n"
            "5. Rules saved automatically!\n\n"
            "*Format Example:*\n"
            "1. No spam\n"
            "2. Be respectful\n"
            "3. No NSFW\n"
            "4. Have fun!\n\n"
            "Members can view with /rules",
            parse_mode='Markdown'
        )
    
    elif data == "send_no_photo":
        if user_id in user_states:
            # প্রোমোশন ডাটাবেসে সেভ করুন
            promo_id = db.add_promotion(
                user_id=user_id,
                user_name=user_states[user_id].get('user_name', 'User'),
                message=user_states[user_id].get('text', ''),
                photo_id=None
            )
            
            if promo_id:
                await query.edit_message_text(
                    "✅ *Promotion Saved!*\n\n"
                    "Your promotion has been saved to database.\n"
                    "In real scenario, I would send it to all my groups!\n\n"
                    "*Test in group:*\n"
                    "1. Add me to a test group\n"
                    "2. I'll send promotions there\n\n"
                    "Thanks for using promotion system!",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text("❌ Failed to save promotion.")
            
            # ক্লিয়ার স্টেট
            if user_id in user_states:
                del user_states[user_id]
    
    elif data == "add_photo":
        if user_id in user_states:
            await query.edit_message_text(
                "📸 *Add Photo*\n\n"
                "Please send me a photo for your promotion.\n"
                "You can add a caption too!\n\n"
                "Type /cancel to cancel.",
                parse_mode='Markdown'
            )
    
    elif data == "confirm_send":
        if user_id in user_states:
            # প্রোমোশন ডাটাবেসে সেভ করুন
            promo_id = db.add_promotion(
                user_id=user_id,
                user_name=user_states[user_id].get('user_name', 'User'),
                message=user_states[user_id].get('text', ''),
                photo_id=user_states[user_id].get('photo_id')
            )
            
            if promo_id:
                await query.edit_message_text(
                    "✅ *Promotion Sent Successfully!*\n\n"
                    "Your promotion has been saved and will be sent to all groups!\n\n"
                    "*To test:*\n"
                    "1. Add me to a test group\n"
                    "2. I'll automatically send promotions\n\n"
                    "Thanks for using our promotion system!",
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text("❌ Failed to save promotion.")
            
            # ক্লিয়ার স্টেট
            if user_id in user_states:
                del user_states[user_id]
    
    elif data == "cancel_promo":
        if user_id in user_states:
            del user_states[user_id]
        await query.edit_message_text("❌ Promotion cancelled.")
# ==================== WELCOME & GOODBYE HANDLERS ====================

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """নতুন মেম্বার ওয়েলকাম করুন"""
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            # বট গ্রুপে যুক্ত হয়েছে
            await update.message.reply_text(
                "🤖 *Thanks for adding me!*\n\n"
                "I can help manage your group. Please make me admin to use all features.\n"
                "Use /help to see available commands.\n\n"
                "*Features:*\n"
                "• Upload rules with /uploadrules\n"
                "• Set welcome with /welcome\n"
                "• Ban/kick users\n"
                "• Promotion system",
                parse_mode='Markdown'
            )
            # ডাটাবেসে গ্রুপ যোগ করুন
            db.add_group(
                group_id=update.effective_chat.id,
                group_name=update.effective_chat.title
            )
        else:
            # সাধারণ ইউজার যোগ হয়েছে
            welcome_msg = db.get_welcome(update.effective_chat.id)
            
            if welcome_msg:
                # ওয়েলকাম মেসেজে ভ্যারিয়েবল রিপ্লেস করুন
                welcome_msg = welcome_msg.replace("{user}", member.mention_html())
                welcome_msg = welcome_msg.replace("{group}", update.effective_chat.title)
                await update.message.reply_text(welcome_msg, parse_mode='HTML')
            else:
                # ডিফল্ট ওয়েলকাম
                await update.message.reply_text(
                    f"👋 Welcome {member.mention_html()} to {update.effective_chat.title}!\n"
                    f"We're glad to have you here! 🎉",
                    parse_mode='HTML'
                )

async def goodbye_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """মেম্বার বিদায় নিলে"""
    if update.message.left_chat_member:
        member = update.message.left_chat_member
        if member.id != context.bot.id:  # বট নিজে রিমুভ হলে না
            await update.message.reply_text(
                f"👋 Goodbye {member.mention_html()}!\n"
                f"We'll miss you! 😢",
                parse_mode='HTML'
            )
# ==================== CANCEL COMMAND ====================

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """হ্যান্ডেল /cancel কমান্ড"""
    user_id = update.effective_user.id
    
    if user_id in user_states:
        action = user_states[user_id].get('action', '')
        del user_states[user_id]
        
        if action == 'uploading_rules':
            await update.message.reply_text("❌ Rules upload cancelled.")
        elif action == 'creating_promotion':
            await update.message.reply_text("❌ Promotion creation cancelled.")
    else:
        await update.message.reply_text("❌ No active operation to cancel.")

# ==================== MAIN FUNCTION ====================

def main():
    """বট শুরু করুন"""
    try:
        # অ্যাপ্লিকেশন তৈরি করুন
        application = Application.builder().token(TOKEN).build()
        
        # কমান্ড হ্যান্ডলার যোগ করুন
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("id", id_command))
        
        # রুলস সিস্টেম
        application.add_handler(CommandHandler("rules", rules_command))
        application.add_handler(CommandHandler("uploadrules", uploadrules_command))
        application.add_handler(CommandHandler("setrules", setrules_command))
        
        # গ্রুপ ম্যানেজমেন্ট
        application.add_handler(CommandHandler("ban", ban_user))
        application.add_handler(CommandHandler("kick", kick_user))
        application.add_handler(CommandHandler("mute", mute_user))
        application.add_handler(CommandHandler("welcome", set_welcome))
        
        # প্রোমোশন সিস্টেম
        application.add_handler(CommandHandler("promotion", promotion_command))
        application.add_handler(CommandHandler("cancel", cancel_command))
        
        # মেসেজ হ্যান্ডলার
        application.add_handler(MessageHandler(
            filters.TEXT & filters.ChatType.PRIVATE & ~filters.COMMAND,
            handle_promotion_text
        ))
        application.add_handler(MessageHandler(
            filters.PHOTO & filters.ChatType.PRIVATE,
            handle_promotion_photo
        ))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_rules_text
        ))
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            welcome_new_member
        ))
        application.add_handler(MessageHandler(
            filters.StatusUpdate.LEFT_CHAT_MEMBER,
            goodbye_member
        ))
        
        # বাটন হ্যান্ডলার
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # বট শুরু করুন
        print("=" * 60)
        print("🤖 UNIVERSAL TELEGRAM BOT")
        print("=" * 60)
        print("✅ Everyone can use - No restrictions!")
        print(f"🔗 Developer: www.x.com/im_shoudo")
        print(f"🔑 Token: {TOKEN}")
        print("=" * 60)
        print("🚀 Bot is starting...")
        print("📝 Features: Rules Upload, Promotion, Group Management")
        print("=" * 60)
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check internet connection")
        print("2. Make sure token is correct")
        print("3. Run: pip install python-telegram-bot")

if __name__ == '__main__':
    main()