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
    filters,
)

from config import TELEGRAM_BOT_TOKEN
from orchestrators.comparator import run_comparison

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

    # Run Workflow 1 — sequential agent pipeline
    try:
        summary = await run_comparison(user_text)
    except Exception:
        logger.exception("Error in comparison pipeline")
        summary = "⚠️ An error occurred while processing your request. Please try again later."

    await context.bot.send_message(chat_id=chat_id, text=summary)


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

    logger.info("Telegram application built successfully.")
    return app
