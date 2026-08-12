#!/usr/bin/env python3
"""
Telegram Bot: SBC24 Score Tracker
Provides live scores, fixtures, and favorite teams management.
Uses python-telegram-bot v20+ (async) with polling.
"""

import logging
import os
from typing import Dict, List

from dotenv import load_dotenv
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set.")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------- Constants ----------
WELCOME_TEXT = (
    "⚽ Welcome to SBC24 Score Tracker Bot!\n\n"
    "Your ultimate companion for real‑time sports scores, live match updates, "
    "and fixtures. Tap a button below to get started instantly!"
)

HELP_TEXT = (
    "📖 *User Guide*\n\n"
    "Use the buttons below or type these commands:\n"
    "/start – Show welcome message\n"
    "/help – Show this guide\n"
    "/scores – Fetch current live scores\n\n"
    "💡 *Tip:* You can save your favorite teams to get quick updates later."
)

MOCK_SCORES = [
    {"home": "Barcelona", "away": "Real Madrid", "score": "2 – 1", "status": "Live"},
    {"home": "Bayern Munich", "away": "Dortmund", "score": "0 – 0", "status": "Half‑time"},
    {"home": "PSG", "away": "Marseille", "score": "3 – 2", "status": "Live"},
]

MOCK_FIXTURES = [
    {"home": "Juventus", "away": "Inter", "time": "20:45 CET"},
    {"home": "Liverpool", "away": "Chelsea", "time": "18:30 CET"},
    {"home": "Ajax", "away": "Feyenoord", "time": "16:00 CET"},
]

MOCK_FAVORITES = ["Barcelona", "Bayern Munich", "Liverpool"]

# ---------- Keyboards ----------
def main_keyboard() -> InlineKeyboardMarkup:
    """Return the main inline keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🔴 Live Scores", callback_data="scores"),
            InlineKeyboardButton("📅 Today's Fixtures", callback_data="fixtures"),
        ],
        [
            InlineKeyboardButton("⭐ Favorite Teams", callback_data="favorites"),
            InlineKeyboardButton("📖 User Guide", callback_data="help"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- Command Handlers ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with the main keyboard."""
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_keyboard(),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the help text."""
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )

async def scores(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetch and display current live scores.
    (Currently uses mock data; replace with real API call.)
    """
    # In a real implementation, you would call your sports API here.
    # For now we simulate a delay and return mock data.
    lines = ["📊 *Live Scores*\n"]
    for match in MOCK_SCORES:
        lines.append(
            f"🏟 {match['home']} vs {match['away']}\n"
            f"   {match['score']}  •  {match['status']}"
        )
    text = "\n\n".join(lines)
    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_keyboard(),
    )

# ---------- Callback Query Handler ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline button presses."""
    query = update.callback_query
    await query.answer()  # acknowledge the callback

    data = query.data
    if data == "scores":
        # Reuse the /scores logic, but send as a new message from the callback
        # We'll reply with the scores.
        lines = ["📊 *Live Scores*\n"]
        for match in MOCK_SCORES:
            lines.append(
                f"🏟 {match['home']} vs {match['away']}\n"
                f"   {match['score']}  •  {match['status']}"
            )
        text = "\n\n".join(lines)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )
    elif data == "fixtures":
        lines = ["📅 *Today's Fixtures*\n"]
        for fixture in MOCK_FIXTURES:
            lines.append(
                f"⚽ {fixture['home']} vs {fixture['away']}\n"
                f"   🕒 {fixture['time']}"
            )
        text = "\n\n".join(lines)
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )
    elif data == "favorites":
        if MOCK_FAVORITES:
            favs = "\n".join(f"⭐ {team}" for team in MOCK_FAVORITES)
            text = f"*Your Favorite Teams*\n\n{favs}"
        else:
            text = "You haven't added any favorite teams yet."
        await query.edit_message_text(
            text,
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )
    elif data == "help":
        await query.edit_message_text(
            HELP_TEXT,
            parse_mode="Markdown",
            reply_markup=main_keyboard(),
        )
    else:
        await query.edit_message_text(
            "Unknown command. Please use the buttons below.",
            reply_markup=main_keyboard(),
        )

# ---------- Error Handler ----------
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ Sorry, something went wrong. Please try again later."
        )

# ---------- Main Application ----------
def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("scores", scores))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Register error handler
    application.add_error_handler(error_handler)

    # Start polling (suitable for Render worker)
    logger.info("Bot started with polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
