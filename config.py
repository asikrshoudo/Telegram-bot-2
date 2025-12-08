import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Token
    BOT_TOKEN = os.getenv("BOT_TOKEN", "8353713232:AAH9c3MLO5z-o3HRDbHOzs453ysfMFrKFkQ")
    
    # Bot Info
    BOT_USERNAME = os.getenv("BOT_USERNAME", "")
    OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))
    
    # Admin IDs
    ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Database
    DB_PATH = "database/groups.db"
    
    @staticmethod
    def validate():
        if not Config.BOT_TOKEN or Config.BOT_TOKEN == "your_bot_token_here":
            raise ValueError("❌ Please set BOT_TOKEN in .env file")
        return True