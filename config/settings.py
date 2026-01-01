"""
Configuration settings for the Telegram bot.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "")

# Admin Configuration
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/bot.db")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")

# Bot Settings
MAX_MESSAGE_LENGTH = 4096
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")
TIMEZONE = os.getenv("TIMEZONE", "UTC")

# Webhook Configuration (if using webhooks)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", "8443"))
WEBHOOK_LISTEN = os.getenv("WEBHOOK_LISTEN", "0.0.0.0")

# Redis Configuration (optional for caching)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# API Keys (if needed for external services)
API_KEYS = {
    "weather": os.getenv("WEATHER_API_KEY", ""),
    "news": os.getenv("NEWS_API_KEY", ""),
}

# Bot Features (enable/disable)
FEATURES = {
    "welcome_message": os.getenv("FEATURE_WELCOME", "true").lower() == "true",
    "admin_commands": os.getenv("FEATURE_ADMIN", "true").lower() == "true",
    "user_commands": os.getenv("FEATURE_USER", "true").lower() == "true",
    "logging": os.getenv("FEATURE_LOGGING", "true").lower() == "true",
}