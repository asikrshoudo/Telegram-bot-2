# 🤖 Telegram Bot 2.0

A modern, feature-rich **Telegram bot** built with Python, designed for scalability and ease of use. Perfect for managing communities, automating tasks, and building interactive experiences.

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Python](https://img.shields.io/badge/Python-3.11+-yellow?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 🚀 **Modern Architecture** – Modular and scalable codebase  
- 🗄️ **Database Support** – SQLAlchemy with PostgreSQL/SQLite  
- 👑 **Admin System** – Role-based access control (RBAC)  
- 📊 **User Management** – Track users, groups, and activities  
- 📝 **Logging** – Comprehensive logging system for debugging  
- 🐳 **Docker Support** – Containerized for easy deployment  
- 🔧 **Webhook/Polling** – Supports both Webhook and Long Polling  
- 🌐 **Multi-language** – Ready for internationalization (i18n)  
- 🔐 **Environment Config** – Secure configuration via `.env`  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher  
- Telegram Bot Token from [@BotFather](https://t.me/botfather)  
- Git (optional)  

### Step 1: Clone the Repository
```bash
git clone https://github.com/asikrshoudo/Telegram-bot-2.git
cd Telegram-bot-2
```

### Step 2: Setup Environment

**Method A: Using Setup Script (Recommended)**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh

```

### Step 3: Configure Your Bot
```bash
cp .env.example .env
```

Edit .env with your details:
`env`
BOT_TOKEN=1234567890:ABCDEFG...
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite:///data/bot.db

### Step 4: Run the Bot

🐍 **Python**
```bash
python main.py

```


