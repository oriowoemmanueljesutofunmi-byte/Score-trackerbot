# SBC24 Score Tracker Bot

A Telegram bot that provides live sports scores, fixtures, and favorite team tracking.  
Built with `python-telegram-bot` and designed for deployment on **Render** via **GitHub**.

## Features

- `/start` – Welcome message with interactive inline keyboard.
- `/help` – User guide.
- `/scores` – Current live scores (mock data, ready for API integration).
- Inline buttons for:
  - Live Scores
  - Today's Fixtures
  - Favorite Teams
  - User Guide

## Deployment on Render

1. **Fork or push this repository** to your GitHub account.

2. **Create a new Web Service** on Render:
   - Connect your GitHub repository.
   - Set the **Environment** to `Python 3`.
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py` (or use the Procfile with `worker: python bot.py`).

3. **Set the Environment Variable**:
   - In the Render dashboard, go to your service → **Environment** → **Environment Variables**.
   - Add a variable:
     - `Key`: `BOT_TOKEN`
     - `Value`: Your Telegram Bot Token (obtain from [@BotFather](https://t.me/BotFather)).

4. **Deploy** – Render will automatically build and run the bot using polling.

## Local Development

1. Clone the repository.
2. Create a `.env` file with your `BOT_TOKEN`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
