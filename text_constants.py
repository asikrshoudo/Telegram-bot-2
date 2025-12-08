# All text messages

START_MESSAGE = """Hi {username}! How can I assist you today?

I can manage your groups or channels.
Also I can promote any of your links, posts, or images!

📋 *Available Commands:*
/start - Start bot
/help - Show help
/id - Get your ID
/promotion - Create promotion

👮 *Admin Commands (in groups):*
/ban - Ban user
/kick - Kick user
/mute - Mute user
/welcome - Set welcome
/rules - Set rules
/about - About developer

📢 *Promotion Feature:*
Send /promotion in private chat with me to create promotions that I'll share in all groups I'm in!
"""

HELP_MESSAGE = """🆘 *Help Center*

*Group Management:*
1. Add me to your group
2. Make me admin with all permissions
3. Use commands like /welcome, /rules, /ban, etc.

*Promotion System:*
1. Message me privately
2. Use /promotion command
3. Send your promotion content
4. I'll share it in all my groups!

*Contact Developer:* @im_shoudo (X.com/im_shoudo)

*Need more help?* Just ask! 😊
"""

ABOUT_MESSAGE = """👨‍💻 *About Developer*

*Developer:* Shoudo
*Twitter/X:* [@im_shoudo](https://ww.x.com/im_shoudo)
*GitHub:* [github.com/shoudo](https://github.com/asikrshoudo)

This bot is designed for efficient group management and promotion automation. Built with Python and python-telegram-bot library.

*Features:*
• Group Management (ban, kick, mute, welcome, rules)
• Promotion Broadcasting
• Multi-group support
• User-friendly interface

*Support:* For any issues, contact @im_shoudo
"""

ERROR_MESSAGES = {
    "no_reply": "❌ Please reply to a user's message!",
    "no_admin": "❌ You need to be admin to use this command!",
    "bot_not_admin": "❌ I need admin permissions to do that!",
    "private_only": "❌ This command only works in private chat!",
    "group_only": "❌ This command only works in groups!",
}