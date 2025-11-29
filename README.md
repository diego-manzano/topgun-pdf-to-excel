# Petron Settlement Report Bot

Telegram bot that extracts transaction data from Petron Merchant Settlement Reports (images or PDFs) and generates formatted Excel files.

## Features

- ✅ Accepts both **images** and **PDFs**
- ✅ Extracts data using **Gemini 2.5 Flash** (free tier)
- ✅ Generates professionally formatted **Excel files**
- ✅ 100% accurate extraction (validated with test data)
- ✅ Free hosting on **GitHub Codespaces** (60 hrs/month)

## Quick Start

### 1. Get API Keys

**Telegram Bot Token:**
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy your bot token

**Gemini API Key:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API Key"
3. Create a new key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

**Option A: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your keys
# TELEGRAM_BOT_TOKEN=your_bot_token_here
# GEMINI_API_KEY=your_gemini_api_key_here
```

**Option B: Export variables directly**

```bash
export TELEGRAM_BOT_TOKEN='your-bot-token-here'
export GEMINI_API_KEY='your-gemini-key-here'
```

### 4. Run the Bot

```bash
python telegram_bot.py
```

## Usage

1. Open your Telegram bot
2. Send `/start` to see instructions
3. Send a photo or PDF of a Petron settlement report
4. Wait 5-10 seconds
5. Download the Excel file!

## Testing

### Test Gemini Extraction (Image)
```bash
python test_extract.py
```

### Test Gemini Extraction (PDF)
```bash
python test_pdf_extraction.py
```

### Test Excel Generation
```bash
python test_excel_generation.py
```

## Deployment

### Option 1: GitHub Codespaces (Free, Recommended)

1. **Create Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   gh repo create topgun-image-to-excel --public --source=. --push
   ```

2. **Create Codespace:**
   - Go to your GitHub repo
   - Click "Code" → "Codespaces" → "Create codespace on main"

3. **Set Secrets:**
   - Go to repo Settings → Secrets → Codespaces
   - Add `TELEGRAM_BOT_TOKEN`
   - Add `GEMINI_API_KEY`

4. **Run Bot:**
   ```bash
   pip install -r requirements.txt
   python telegram_bot.py
   ```

5. **Keep Running:**
   - Codespace stays active while you're connected
   - Free tier: 60 hours/month (2 hours/day)

### Option 2: Railway.app (500 hrs/month free)

1. Create account at [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Add environment variables in Settings
4. Deploy!

### Option 3: Render.com (Free tier)

1. Create account at [render.com](https://render.com)
2. New Web Service → Connect GitHub
3. Add environment variables
4. Deploy!

### Option 4: Local Machine (24/7)

```bash
# Run in background
nohup python telegram_bot.py > bot.log 2>&1 &

# Check status
tail -f bot.log

# Stop bot
pkill -f telegram_bot.py
```

## Project Structure

```
topgun-image-to-excel/
├── telegram_bot.py           # Main bot application
├── test_extract.py           # Test image extraction
├── test_pdf_extraction.py    # Test PDF extraction
├── test_excel_generation.py  # Test Excel generation
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## API Costs

**Free Tier Limits (Gemini 2.5 Flash):**
- 15 requests per minute
- 1 million tokens per day
- 1,500 requests per day

**Expected Usage:**
- ~50-100 reports/day = **$0/month** (well within free tier)

**Telegram Bot API:**
- Completely free, unlimited messages

## Troubleshooting

### Bot Not Responding
```bash
# Check if bot is running
ps aux | grep telegram_bot

# Check logs
tail -f bot.log
```

### Extraction Errors
- Ensure image/PDF is clear and readable
- Check if all transaction rows are visible
- Verify it's a standard Petron settlement report

### API Quota Exceeded
- Gemini free tier: 15 requests/minute
- Wait 60 seconds and try again
- Consider upgrading to paid tier if needed

## Features & Validation

**Tested with sample data:**
- ✅ 17/17 transactions extracted
- ✅ All amounts match exactly
- ✅ Header info parsed correctly
- ✅ Excel formatting professional
- ✅ Both images and PDFs work

## Support

For issues or questions:
1. Check the logs (`bot.log`)
2. Review error messages in Telegram
3. Verify API keys are set correctly
4. Ensure dependencies are installed

## License

MIT License - Free to use and modify
