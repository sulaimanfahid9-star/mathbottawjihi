# Tawjihi Math Bot 📚🤖

An automated Telegram bot that posts one math question per day with step-by-step Arabic solutions powered by Google Gemini AI.

## Features

✅ **Automated Daily Posts** - Posts 5 questions per day at scheduled times
✅ **AI-Powered Solutions** - Uses Google Gemini AI to generate clear Arabic explanations
✅ **Comprehensive Database** - 4,272 questions covering all Grade 12 math topics
✅ **Smart Variant Generation** - Creates new question variants when database is exhausted
✅ **GitHub Actions Integration** - Fully automated with no manual intervention needed
✅ **Logging & Monitoring** - Detailed logs for tracking bot performance
✅ **Database Persistence** - Tracks used questions to avoid repetition

## Bot Details

- **Bot Name:** @tawjihi_ma_bot
- **Bot Token:** `8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek`
- **Channel:** https://t.me/tawjihisu
- **Language:** Questions in English, Solutions in Arabic

## Project Structure

```
tawjihi_bot/
├── main.py                          # Core bot application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── data/
│   └── questions.json              # Question database (4,272 questions)
├── logs/
│   └── bot.log                     # Bot execution logs
└── .github/
    └── workflows/
        └── post-daily-question.yml # GitHub Actions workflow
```

## Database Structure

Each question in `data/questions.json` has the following structure:

```json
{
  "id": 1,
  "question": "Solve the equation 2x + 5 = 15",
  "type": "algebra",
  "chapter": "نظريتا الباقي والعوامل",
  "source": "Grade 12 Math, Sem 1, Unit 1, Advanced Section",
  "used": false
}
```

**Fields:**
- `id` - Unique question identifier
- `question` - Math question in English
- `type` - Question type: "algebra", "calculus", or "geometry"
- `chapter` - Chapter name in Arabic
- `source` - Source reference
- `used` - Boolean flag (true = already posted, false = available)

## Setup Instructions

### 1. Prerequisites

- Python 3.11+
- GitHub account with repository access
- Telegram Bot Token (already created: `8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek`)
- Google Gemini API Key (provided: `AIzaSyDl84Xn_G8Z6Fdd2yVwQkga1QAWQtTfXyg`)
- Telegram Channel ID (for posting)

### 2. Local Testing

```bash
# Clone the repository
git clone https://github.com/sulaimanfahid9-star/mathbottawjihi.git
cd mathbottawjihi

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TELEGRAM_BOT_TOKEN="8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek"
export TELEGRAM_CHAT_ID="YOUR_CHANNEL_ID"
export GEMINI_API_KEY="AIzaSyDl84Xn_G8Z6Fdd2yVwQkga1QAWQtTfXyg"

# Run the bot
python main.py
```

### 3. GitHub Setup

#### Step 1: Add Secrets to GitHub Repository

1. Go to your GitHub repository: `https://github.com/sulaimanfahid9-star/mathbottawjihi`
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

| Secret Name | Value |
|---|---|
| `TELEGRAM_BOT_TOKEN` | `8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek` |
| `TELEGRAM_CHAT_ID` | Your Telegram channel ID (e.g., `-1001234567890`) |
| `GEMINI_API_KEY` | `AIzaSyDl84Xn_G8Z6Fdd2yVwQkga1QAWQtTfXyg` |

#### Step 2: Find Your Telegram Channel ID

To find your channel ID, you can:

1. **Method 1:** Send a message to your channel, then visit:
   ```
   https://api.telegram.org/bot8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek/getUpdates
   ```
   Look for the `chat` object and note the `id` field.

2. **Method 2:** Use a bot like `@userinfobot` in your channel to get the ID.

#### Step 3: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. Click **"I understand my workflows, go ahead and enable them"**
3. The workflow will automatically run on the scheduled times

### 4. Posting Schedule

The bot posts at the following times (UTC):

| Time | Cron Expression |
|---|---|
| 08:00 UTC | `0 8 * * *` |
| 10:00 UTC | `0 10 * * *` |
| 12:00 UTC | `0 12 * * *` |
| 16:00 UTC | `0 16 * * *` |
| 20:00 UTC | `0 20 * * *` |

To adjust times, edit `.github/workflows/post-daily-question.yml`

## How It Works

### Daily Workflow (Per Execution)

1. **Load Database** - Reads all questions from `data/questions.json`
2. **Select Question** - Finds the first unused question (where `used = false`)
3. **Generate Solution** - Uses Gemini AI to create a step-by-step Arabic solution
4. **Generate Tip** - Creates a short educational tip in Arabic
5. **Format Post** - Combines question, solution, and tip into Telegram format
6. **Send to Telegram** - Posts the formatted message to the channel
7. **Mark as Used** - Sets `used = true` for the question
8. **Save Database** - Commits changes back to GitHub

### When Database is Exhausted

When all questions are marked as `used = true`:

1. The bot randomly selects a used question
2. Uses Gemini AI to generate a variant (same concept, different numbers)
3. Assigns a new unique ID
4. Adds it to the database with `used = false`
5. Continues the normal posting cycle

**Example:**
- Original: "Solve 3x + 7 = 19"
- Variant: "Solve 5x + 11 = 31"

## Solution Format

Each solution follows this structure:

```
1. المعادلة الأصلية:
   [Original equation/problem]

2. الخطوة الأولى: [Description]
   [Mathematical work]

3. الخطوة الثانية: [Description]
   [Mathematical work]

...

✅ النتيجة النهائية:
[Final answer]
```

## Error Handling

- **Telegram Failure** - Logs error and retries once
- **Gemini Failure** - Logs error and skips posting
- **Database Error** - Logs error and exits gracefully
- **All errors are logged** to `logs/bot.log`

## Monitoring & Logs

Logs are saved to `logs/bot.log` with the following information:

```
2026-02-03 18:05:30,123 - INFO - Tawjihi Math Bot - Starting Daily Post
2026-02-03 18:05:31,456 - INFO - Loading question database...
2026-02-03 18:05:32,789 - INFO - Loaded 4272 questions from database
2026-02-03 18:05:33,012 - INFO - Selected question 1: Find the remainder...
2026-02-03 18:05:45,678 - INFO - Solution generated successfully
2026-02-03 18:05:47,890 - INFO - Daily tip generated
2026-02-03 18:05:48,123 - INFO - Message sent successfully to Telegram
2026-02-03 18:05:49,456 - INFO - Daily post completed successfully!
```

## Database Statistics

**Total Questions:** 4,272
**Questions per Chapter:** 178

**Chapters Covered:**

| Chapter | Questions | Type |
|---|---|---|
| نظريتا الباقي والعوامل | 178 | Algebra |
| الكسور الجزئية | 178 | Algebra |
| المتطابقات المثلثية 1 | 178 | Algebra |
| المتطابقات المثلثية 2 | 178 | Algebra |
| حل المعادلات المثلثية | 178 | Algebra |
| مشتقة اقترانات خاصة | 178 | Calculus |
| مشتقتا القرب والقسمة والمشتقات العليا | 178 | Calculus |
| قاعدة السلسلة | 178 | Calculus |
| الاشتقاق الضمني | 178 | Calculus |
| المعدلات المرتبطة | 178 | Calculus |
| الأعداد المركبة | 178 | Algebra |
| العمليات على الأعداد المركبة | 178 | Algebra |
| البحل الهندسي في المستوى المركب | 178 | Geometry |
| تكامل اقترانات خاصة | 178 | Calculus |
| التكامل بالتعويض | 178 | Calculus |
| التكامل بالكسور الجزئية | 178 | Calculus |
| التكامل بالأجزاء | 178 | Calculus |
| المساحات والحجوم | 178 | Calculus |
| المعادلات التفاضلية | 178 | Calculus |
| المنحنيات في الفضاء | 178 | Geometry |
| المستقيمات في الفضاء | 178 | Geometry |
| الضرب القياسي | 178 | Geometry |
| التوزيع الهندسي وتوزيع ذي الحدّين | 178 | Algebra |
| التوزيع الطبيعي | 178 | Algebra |

## Troubleshooting

### Bot not posting?

1. **Check GitHub Actions:** Go to Actions tab and check workflow runs
2. **Verify Secrets:** Ensure all three secrets are set correctly
3. **Check Logs:** Download artifacts from failed runs to see error details
4. **Test Locally:** Run `python main.py` locally with environment variables set

### Questions not changing?

1. **Check database:** Verify `data/questions.json` is being updated
2. **Check used flag:** Ensure questions have `"used": true` after posting
3. **Regenerate variants:** If all questions are used, bot will auto-generate variants

### Telegram not receiving messages?

1. **Verify Channel ID:** Make sure you have the correct channel ID
2. **Check Bot Permissions:** Ensure bot has permission to post in the channel
3. **Test API:** Manually test with:
   ```bash
   curl -X POST https://api.telegram.org/bot8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek/sendMessage \
     -d chat_id=YOUR_CHANNEL_ID \
     -d text="Test message"
   ```

## API References

- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Google Gemini API:** https://ai.google.dev/
- **GitHub Actions:** https://docs.github.com/en/actions

## License

MIT License - Feel free to use and modify

## Support

For issues or questions:
1. Check the logs in `logs/bot.log`
2. Review GitHub Actions workflow runs
3. Verify all environment variables are set correctly

---

**Bot Status:** ✅ Active and Running
**Last Updated:** 2026-02-03
**Questions in Database:** 4,272
**Posting Frequency:** 5 times per day
