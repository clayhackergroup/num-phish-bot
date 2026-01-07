# Telegram Verification Bot

A Telegram bot that verifies users by requesting contact sharing.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Get your bot token from BotFather on Telegram

3. Find your admin Telegram ID (use @userinfobot or @getidsbot)

4. Update configuration in `bot.py`:
   - Replace `BOT_TOKEN` with your bot token
   - Replace `ADMIN_ID` with your admin ID
   - Set `ACCOUNT_NAME` and `MOBILE_NUMBER`

5. Run the bot:
```bash
python bot.py
```

## Features

- `/start` - Shows welcome message with verify button
- Verify button - Requests user to share contact via Telegram's native contact picker
- Admin notification - Sends shared contact to admin
- Clean UI with emoji indicators

## How it works

1. User types `/start`
2. Bot sends welcome message with "Verify - Share Contact" button
3. User clicks button → Telegram's contact picker opens
4. User confirms contact sharing
5. Bot receives contact and forwards it to admin
6. Admin receives contact info with user details
