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
from orchestrators.reporter_workflow import run_report_workflow
from agents.reporter import ReporterAgent
from agents.search_agent import SearchAgent
from services.storage import load_settings, save_settings
from services.search import perform_search

logger = logging.getLogger(__name__)

# Telegram's hard limit per message
_MAX_MSG_LEN = 4096


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _send_long(
    bot,
    chat_id: int | str,
    text: str,
    parse_mode: str | None = "Markdown",
) -> None:
    """Send *text*, splitting into chunks if it exceeds Telegram's 4096-char limit.

    Splits on newlines where possible to avoid cutting mid-sentence.
    Falls back to plain text if the Markdown parse fails.
    """
    chunks: list[str] = []
    remaining = text
    while len(remaining) > _MAX_MSG_LEN:
        # Try to split at the last newline within the limit
        split_at = remaining.rfind("\n", 0, _MAX_MSG_LEN)
        if split_at == -1:
            split_at = _MAX_MSG_LEN
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")
    chunks.append(remaining)

    for chunk in chunks:
        if not chunk.strip():
            continue
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=chunk,
                parse_mode=parse_mode,
            )
        except Exception:
            # Markdown parse error — retry as plain text
            await bot.send_message(chat_id=chat_id, text=chunk)


async def _send_agent_results(
    bot,
    chat_id: int | str,
    results: list[dict[str, str]],
) -> None:
    """Send each agent result as a separate Telegram message with a styled header."""
    for entry in results:
        icon = entry.get("icon", "🤖")
        name = entry.get("name", "Agent")
        content = entry.get("content", "")

        # Bold header via Markdown
        header = f"*{icon} {name}*"
        full_text = f"{header}\n\n{content}"

        await _send_long(bot, chat_id, full_text, parse_mode="Markdown")


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

    # Special trigger: "web search"
    if user_text.lower().strip() == "web search":
        await _handle_web_search_command(update, context)
        return

    # Special trigger: "change city"
    if user_text.lower().strip() == "change city":
        context.user_data["awaiting_city"] = True
        await update.message.reply_text("🏙️ Which city would you like to set for the reports?")
        return

    # Handle city entry if we are awaiting it
    if context.user_data.get("awaiting_city"):
        new_city = user_text.strip()
        settings = load_settings()
        settings["city"] = new_city
        save_settings(settings)
        
        context.user_data["awaiting_city"] = False
        await update.message.reply_text(f"✅ City updated to *{new_city}*. The next report will focus on this location.", parse_mode="Markdown")
        return

    # Typing indicator — shows "typing…" while agents work
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Run Workflow 1 — parallel agent pipeline (streaming)
    try:
        async for result in run_comparison(user_text):
            # Send each agent's response as soon as it's ready
            await _send_agent_results(context.bot, chat_id, [result])
    except Exception:
        logger.exception("Error in comparison pipeline")
        await context.bot.send_message(
            chat_id=chat_id,
            text="⚠️ An error occurred while processing your request. Please try again later.",
        )


async def _handle_report_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Trigger Workflow 2 manually."""
    if update.message is None:
        return

    chat_id = update.message.chat_id
    logger.info("Manual report trigger requested from chat %s.", chat_id)

    # 1. Send the status message and store it
    status_msg = await context.bot.send_message(
        chat_id=chat_id,
        text="🔄 Generating report summary... Please wait.",
    )

    try:
        # 2. Run the workflow
        commentary = await run_report_workflow()
        
        # 3. Add header (bold name + icon) and send the final report
        header = f"*{ReporterAgent.ICON} {ReporterAgent.DISPLAY_NAME}*"
        full_text = f"{header}\n\n{commentary}"
        await _send_long(context.bot, chat_id, full_text)
        
        # 4. Delete the initial status message to keep the chat clean
        await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)

    except Exception:
        logger.exception("Manual report summary failed.")
        
        # Try to cleanup the status message even on failure
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)
        except Exception:
            pass

        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ Sorry, I couldn't generate the report right now.",
        )


async def _handle_web_search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Perform a web search for green topics in the registered city."""
    if update.message is None:
        return

    chat_id = update.message.chat_id
    
    # 1. Get current city
    settings = load_settings()
    from config import AIR_QUALITY_LOCATION
    city = settings.get("city") or AIR_QUALITY_LOCATION

    logger.info("Web search requested for city: %s", city)

    # 2. Show typing status
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    status_msg = await context.bot.send_message(
        chat_id=chat_id,
        text=f"🌐 Searching for the latest green news in *{city}*...",
        parse_mode="Markdown"
    )

    try:
        # 3. Perform search
        query = f'"{city}" sustainability environment "climate change"'
        results = perform_search(query, max_results=8)

        if not results:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text=f"Sorry, I couldn't find any recent green news for {city} right now."
            )
            return

        # 4. Process with SearchAgent
        search_agent = SearchAgent()
        # Format results for the agent
        formatted_results = "\n\n".join([f"Title: {r['title']}\nLink: {r['href']}\nSnippet: {r['body']}" for r in results])
        
        agent_input = f"City: {city}\n\nSearch Results:\n{formatted_results}"
        commentary = await search_agent.generate(agent_input)

        # 5. Send final message
        header = f"*{SearchAgent.ICON} {SearchAgent.DISPLAY_NAME}*"
        full_text = f"{header}\n\n{commentary}"
        
        await _send_long(context.bot, chat_id, full_text, parse_mode="Markdown")
        
        # 6. Delete status message
        await context.bot.delete_message(chat_id=chat_id, message_id=status_msg.message_id)

    except Exception:
        logger.exception("Web search failed.")
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=status_msg.message_id,
            text="❌ An error occurred during the web search."
        )


# ---------------------------------------------------------------------------
# Helper — send an arbitrary message (used by Workflow 2 / scheduler)
# ---------------------------------------------------------------------------

async def send_message(application: Application, chat_id: str | int, text: str) -> None:
    """Send *text* to *chat_id*, chunking if needed."""
    await _send_long(application.bot, chat_id, text)


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
