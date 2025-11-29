#!/bin/bash
# Quick start script for Petron Settlement Report Bot

echo "🚀 Petron Settlement Report Bot - Quick Start"
echo "=============================================="
echo ""

# Install dependencies if needed
if ! python -c "import telegram" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Check for .env file
if [ -f .env ]; then
    echo "✅ Found .env file"
    echo ""
else
    # Check if environment variables are set
    if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$GEMINI_API_KEY" ]; then
        echo "❌ No .env file found and environment variables not set!"
        echo ""
        echo "Setup steps:"
        echo "1. Copy .env.example to .env:"
        echo "   cp .env.example .env"
        echo ""
        echo "2. Edit .env and add your keys:"
        echo "   TELEGRAM_BOT_TOKEN=your-bot-token"
        echo "   GEMINI_API_KEY=your-gemini-key"
        echo ""
        echo "OR export them directly:"
        echo "   export TELEGRAM_BOT_TOKEN='your-token'"
        echo "   export GEMINI_API_KEY='your-key'"
        echo ""
        exit 1
    else
        echo "✅ Environment variables set"
        echo ""
    fi
fi

echo "🤖 Starting bot..."
echo ""
python telegram_bot.py
