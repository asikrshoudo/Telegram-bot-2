
# 🤖 Telegram Bot 2.0

A modern, feature-rich Telegram bot built with Python, designed for scalability and ease of use. Perfect for managing communities, automating tasks, and building interactive experiences.

![Bot Demo](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🚀 **Modern Architecture** - Modular and scalable codebase.
- 🗄️ **Database Support** - SQLAlchemy with PostgreSQL/SQLite support.
- 👑 **Admin System** - Role-based access control (RBAC).
- 📊 **User Management** - Track users, groups, and activities efficiently.
- 📝 **Logging** - Comprehensive logging system for debugging.
- 🐳 **Docker Support** - Containerized for easy deployment.
- 🔧 **Webhook/Polling** - Supports both Webhook and Long Polling.
- 🌐 **Multi-language** - Ready for internationalization (i18n).
- 🔐 **Environment Config** - Secure configuration via `.env`.

---

## 🚀 Quick Start

### Prerequisites
* Python 3.11 or higher
* Telegram Bot Token from [@BotFather](https://t.me/botfather)
* Git (optional)

### Step 1: Clone the Repository
```bash
git clone [https://github.com/asikrshoudo/Telegram-bot-2.git](https://github.com/asikrshoudo/Telegram-bot-2.git)
cd Telegram-bot-2
```


Step 2: Setup Environment
📝 Method A: Using Setup Script (Recommended)
# Make the script executable
```
chmod +x scripts/setup.sh
```

# Run the setup script
```
./scripts/setup.sh
```

📝 Method B: Manual Setup
 * Create virtual environment:
   # Linux/macOS
```
python -m venv venv
source venv/bin/activate
```
# Windows
```
python -m venv venv
venv\Scripts\activate
```
 * Install dependencies:
```
   pip install -r requirements.txt
```
 * Create necessary directories:
```
   mkdir -p data logs
```
Step 3: Configure Your Bot
 * Get your bot token from @BotFather.
 * Configure environment variables:
   # Copy the example file
```
cp .env.example .env
```
 * Edit the .env file with your details:
   # REQUIRED: Your bot token
BOT_TOKEN=1234567890:ABCDEFG...

# REQUIRED: Admin user IDs (comma-separated)
ADMIN_IDS=123456789,987654321

# Database configuration
DATABASE_URL=sqlite:///data/bot.db

Step 4: Run the Bot
🐍 Running with Python:
```
python main.py
```
🐳 Running with Docker:
# Build and run with Docker Compose
```
docker-compose up -d
```
# Check logs
```
docker-compose logs -f
```
📖 Usage
Basic Commands
 * /start - Start the bot
 * /help - Show help message
 * /about - About this bot
Admin Commands
 * /admin - Access admin panel (Admin only)
 * /stats - View bot statistics (Admin only)
⚙️ Configuration Details
| Variable | Description | Required | Default |
|---|---|---|---|
| BOT_TOKEN | Telegram bot token from @BotFather | ✅ | - |
| ADMIN_IDS | Comma-separated admin IDs | ✅ | - |
| DATABASE_URL | Database connection string | ❌ | sqlite:///data/bot.db |
| LOG_LEVEL | Logging level (DEBUG, INFO, ERROR) | ❌ | INFO |
| REDIS_URL | Redis connection URL | ❌ | - |
🔧 Development
Adding New Commands
 * Edit src/handlers/user_handlers.py for user commands.
 * Edit src/handlers/admin_handlers.py for admin commands.
 * Register the handlers in the main entry point.
Running Tests
python -m pytest tests/

Code Style
black .
isort .
flake8 src/

🐛 Troubleshooting
 * BOT_TOKEN error: Double-check your .env file for typos.
 * ModuleNotFoundError: Ensure your virtual environment is active.
 * Database error: Ensure the data/ directory exists and has write permissions.
🤝 Contributing
 * Fork the repository.
 * Create a feature branch: git checkout -b feature/amazing-feature.
 * Commit changes: git commit -m 'Add amazing feature'.
 * Push to branch: git push origin feature/amazing-feature.
 * Open a Pull Request.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
👨‍💻 Developer
 * GitHub: @asikrshoudo
 * Twitter/X: @im_shoudo
⭐ If you find this project helpful, please give it a star!



