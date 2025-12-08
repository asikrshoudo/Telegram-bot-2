import os
import sys

print("🤖 Telegram Bot Setup Script")
print("=" * 50)

# Create required directories
dirs = ['database', 'handlers', 'utils', 'logs']
for dir_name in dirs:
    os.makedirs(dir_name, exist_ok=True)
    print(f"✅ Created directory: {dir_name}")

# Check .env
if not os.path.exists('.env'):
    print("\n❌ .env file not found!")
    print("Creating .env file...")
    
    env_content = '''# Telegram Bot Configuration
BOT_TOKEN="8353713232:AAH9c3MLO5z-o3HRDbHOzs453ysfMFrKFkQ"
OWNER_ID="YOUR_USER_ID_HERE"  # Change this to your Telegram ID
BOT_USERNAME=""
ADMIN_IDS=""
LOG_LEVEL="INFO"'''
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file")
    print("⚠️  Please edit .env and set your OWNER_ID")
else:
    print("✅ .env file exists")

# Check requirements
print("\n📦 Installing requirements...")
os.system("pip install python-telegram-bot python-dotenv")

print("\n" + "=" * 50)
print("🎉 Setup Complete!")
print("\nNext Steps:")
print("1. Edit .env file and set your OWNER_ID")
print("2. Run: python bot.py")
print("3. Add bot to your Telegram group")
print("4. Make bot admin")
print("5. Use /start command")
print("=" * 50)