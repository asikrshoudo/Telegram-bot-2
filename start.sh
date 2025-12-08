#!/data/data/com.termux/files/usr/bin/bash

echo "🚀 Starting Telegram Group Manager Bot..."
cd ~/storage/emulated/0/Telegram_Bot

# Check Python
if ! command -v python &> /dev/null; then
    echo "Installing Python..."
    pkg install python -y
fi

# Install requirements
pip install python-telegram-bot python-dotenv

# Run bot
echo "🤖 Bot is starting..."
python bot.py
