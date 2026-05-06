"""
Telegram Bot service — builds the bot application, registers handlers,
and provides a helper to send messages to any chat.
"""

from __future__ import annotations

import logging

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from orchestrators.comparator import run_comparison
from orchestrators.weekly_summary import run_weekly_summary

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Message handler (Workflow 1 entry point)
# ---------------------------------------------------------------------------

async def _handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive a user message, run the multi-agent comparator, reply."""
    if update.message is None or update.message.text is None:
        return

    user_text = update.message.text
    chat_id = update.message.chat_id

    logger.info("Received message from chat %s: %s", chat_id, user_text[:80])

    # Special trigger: "report"
    if user_text.lower().strip() == "report":
        await _handle_report_command(update, context)
        return

    # Run Workflow 1 — sequential agent pipeline
    try:
        summary = await run_comparison(user_text)
    except Exception:
        logger.exception("Error in comparison pipeline")
        summary = "⚠️ An error occurred while processing your request. Please try again later."

    await context.bot.send_message(chat_id=chat_id, text=summary)


async def _handle_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trigger Workflow 2 manually."""
    if update.message is None:
        return

    chat_id = update.message.chat_id
    logger.info("Manual report trigger requested from chat %s.", chat_id)

    await context.bot.send_message(chat_id=chat_id, text="🔄 Generating weekly report summary... Please wait.")

    try:
        commentary = await run_weekly_summary()
        await context.bot.send_message(chat_id=chat_id, text=commentary)
    except Exception:
        logger.exception("Manual weekly summary failed.")
        await context.bot.send_message(chat_id=chat_id, text="❌ Sorry, I couldn't generate the report right now.")


# ---------------------------------------------------------------------------
# Helper — send an arbitrary message (used by Workflow 2)
# ---------------------------------------------------------------------------

async def send_message(application: Application, chat_id: str | int, text: str) -> None:
    """Send *text* to *chat_id* via the bot instance owned by *application*."""
    await application.bot.send_message(chat_id=chat_id, text=text)


# ---------------------------------------------------------------------------
# Bot factory
# ---------------------------------------------------------------------------

def build_application() -> Application:
    """Create and configure the ``python-telegram-bot`` Application."""
    app = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    # Register a handler for all non-command text messages
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, _handle_message)
    )

    # Register the /report command
    app.add_handler(CommandHandler("report", _handle_report_command))

    logger.info("Telegram application built successfully.")
    return app
