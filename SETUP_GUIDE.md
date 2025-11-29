# Quick Setup Guide

## Step-by-Step Setup (5 minutes)

### 1. Get Your API Keys

#### Telegram Bot Token
1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Choose a name (e.g., "Top Gun Settlement Bot")
5. Choose a username (e.g., "topgun_settlement_bot")
6. Copy the token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

#### Gemini API Key
1. Go to [https://aistudio.google.com/](https://aistudio.google.com/)
2. Click "Get API Key" in the top right
3. Click "Create API key in new project"
4. Copy the key

### 2. Setup Project

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env file with your favorite editor
nano .env
# or
code .env
# or
vim .env
```

**In your .env file, replace the placeholders:**
```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
GEMINI_API_KEY=AIzaSyA-Your-Actual-Key-Here
```

Save and close the file.

### 3. Run the Bot

```bash
# Option 1: Use the start script
./start_bot.sh

# Option 2: Run directly
python telegram_bot.py
```

### 4. Test It!

1. Open Telegram
2. Search for your bot username
3. Send `/start`
4. Send a test image or PDF
5. Get your Excel file!

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### ".env file not found"
```bash
cp .env.example .env
# Then edit .env with your keys
```

### "Bot token invalid"
- Check that you copied the entire token from BotFather
- Make sure there are no extra spaces in your .env file
- Token format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### "Gemini API error"
- Verify your API key is correct
- Check you haven't exceeded free tier limits (15 requests/minute)
- Make sure the key is active in Google AI Studio

## What Happens When You Send a File?

```
User sends image/PDF
       ↓
Bot receives file
       ↓
Gemini extracts data (5-10 seconds)
       ↓
Excel file generated
       ↓
Bot sends Excel back to user
```

## Free Tier Limits

**Gemini 2.5 Flash:**
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per day

**Expected usage for ~100 reports/day:**
- Cost: $0 (well within free tier)

## Deployment Options

Once working locally, you can deploy to:
1. **GitHub Codespaces** - 60 hrs/month free
2. **Railway.app** - 500 hrs/month free
3. **Render.com** - Free tier available
4. **Your local machine** - Run 24/7

See README.md for deployment instructions.
