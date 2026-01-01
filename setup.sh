#!/bin/bash
# Setup script for Telegram bot

set -e

echo "🚀 Setting up Telegram Bot..."

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p data logs

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your bot token!"
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your BOT_TOKEN"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the bot: python main.py"
echo ""
echo "🐳 For Docker setup: docker-compose up -d"

