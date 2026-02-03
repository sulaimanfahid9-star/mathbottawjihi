# GitHub Actions Secrets Setup Guide

## ⚠️ IMPORTANT: Complete This Step First

Before the bot can run automatically, you must add the required secrets to your GitHub repository.

## Step 1: Go to Repository Settings

1. Open: https://github.com/sulaimanfahid9-star/mathbottawjihi
2. Click on **Settings** (top menu)
3. In the left sidebar, click **Secrets and variables** → **Actions**

## Step 2: Add Three Secrets

Click **"New repository secret"** and add each of the following:

### Secret 1: TELEGRAM_BOT_TOKEN

| Field | Value |
|---|---|
| **Name** | `TELEGRAM_BOT_TOKEN` |
| **Secret** | `8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek` |

Click **Add secret**

### Secret 2: TELEGRAM_CHAT_ID

| Field | Value |
|---|---|
| **Name** | `TELEGRAM_CHAT_ID` |
| **Secret** | Your Telegram channel ID (see below) |

**How to find your Telegram Channel ID:**

#### Option A: Using Telegram Bot API (Recommended)

1. Send a message to your channel
2. Visit this URL in your browser:
   ```
   https://api.telegram.org/bot8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek/getUpdates
   ```
3. Look for the `"chat"` object and find the `"id"` field
4. It will look like: `-1001234567890` (negative number for channels)

#### Option B: Using @userinfobot

1. Add @userinfobot to your Telegram channel
2. It will show you the channel ID
3. Copy the ID (format: `-100...`)

#### Option C: Manual Method

1. Forward a message from your channel to @userinfobot
2. It will display the channel ID

**Example Channel IDs:**
- Private Channel: `-1001234567890`
- Public Channel: `@channelname` (but use the numeric ID)

Click **Add secret**

### Secret 3: GEMINI_API_KEY

| Field | Value |
|---|---|
| **Name** | `GEMINI_API_KEY` |
| **Secret** | `AIzaSyDl84Xn_G8Z6Fdd2yVwQkga1QAWQtTfXyg` |

Click **Add secret**

## Step 3: Verify Secrets Are Added

After adding all three secrets, you should see:

```
✓ TELEGRAM_BOT_TOKEN
✓ TELEGRAM_CHAT_ID
✓ GEMINI_API_KEY
```

## Step 4: Enable GitHub Actions

1. Go to **Actions** tab in your repository
2. You should see the workflow: **"Post Daily Math Question"**
3. If you see a message "Actions are disabled", click **"I understand my workflows, go ahead and enable them"**

## Step 5: Test the Bot

### Option A: Manual Trigger (Recommended for Testing)

1. Go to **Actions** tab
2. Click **"Post Daily Math Question"** workflow
3. Click **"Run workflow"** button
4. Select **"Run workflow"**
5. Wait 30-60 seconds for execution
6. Check your Telegram channel for the posted question

### Option B: Wait for Scheduled Run

The bot will automatically run at these times (UTC):
- 08:00
- 10:00
- 12:00
- 16:00
- 20:00

## Troubleshooting

### Secrets Not Working?

1. **Check spelling:** Secret names are case-sensitive
2. **No extra spaces:** Ensure no leading/trailing spaces in values
3. **Correct values:** Double-check each secret value
4. **Refresh:** Sometimes GitHub takes a minute to register secrets

### Workflow Not Running?

1. **Check Actions tab:** Go to Actions and see if there are any errors
2. **Check workflow file:** Ensure `.github/workflows/post-daily-question.yml` exists
3. **Enable Actions:** Make sure Actions are enabled in repository settings

### Bot Not Posting to Telegram?

1. **Verify Channel ID:** Test with @userinfobot
2. **Check Bot Permissions:** Ensure bot can post in the channel
3. **Test Token:** Visit:
   ```
   https://api.telegram.org/bot8279965776:AAFe4h5Y14wM77CUOUJ3CVf6RA7REB0oWek/getMe
   ```
   Should return bot information

### Logs Not Showing?

1. Go to **Actions** tab
2. Click the failed/completed workflow run
3. Click **"Post Daily Math Question"** job
4. Scroll down to see logs
5. Download artifacts to see `bot.log`

## Security Notes

⚠️ **IMPORTANT:**

- **Never** commit secrets to the repository
- **Never** share your Telegram bot token publicly
- **Never** share your Gemini API key publicly
- Secrets are encrypted by GitHub and only visible to authorized users
- GitHub Actions can only access secrets within workflow runs

## Next Steps

1. ✅ Add all three secrets
2. ✅ Enable GitHub Actions
3. ✅ Test with manual trigger
4. ✅ Monitor first automated run
5. ✅ Check logs for any issues

## Support

If you encounter issues:

1. Check the logs in the Actions tab
2. Verify all secrets are correct
3. Ensure bot has permission to post in channel
4. Review README.md for troubleshooting section

---

**Status:** Ready for configuration
**Next:** Add secrets and test!
