"""
Weekly scheduler — triggers the air quality summary pipeline
on a configurable weekly cadence using APScheduler.
"""

from __future__ import annotations

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import (
    TELEGRAM_CHAT_ID,
    WEEKLY_REPORT_DAY,
    WEEKLY_REPORT_HOUR,
    WEEKLY_REPORT_MINUTE,
)
from orchestrators.weekly_summary import run_weekly_summary

logger = logging.getLogger(__name__)

# Reference kept so main.py can pass the Telegram application later.
_telegram_app = None


def set_telegram_app(app) -> None:  # noqa: ANN001
    """Store a reference to the Telegram Application for sending messages."""
    global _telegram_app
    _telegram_app = app


async def _weekly_job() -> None:
    """Scheduled callback: run Workflow 2 and send the result to Telegram."""
    logger.info("Weekly scheduler triggered.")

    try:
        commentary = await run_weekly_summary()
    except Exception:
        logger.exception("Weekly summary pipeline failed.")
        return

    if _telegram_app is None:
        logger.error("Telegram application not set — cannot send weekly report.")
        return

    try:
        await _telegram_app.bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=commentary,
        )
        logger.info("Weekly report sent to chat %s.", TELEGRAM_CHAT_ID)
    except Exception:
        logger.exception("Failed to send weekly report via Telegram.")


def create_scheduler() -> AsyncIOScheduler:
    """Create and return a configured :class:`AsyncIOScheduler`.

    The scheduler is **not** started here — call ``scheduler.start()``
    from the main entry point after the event loop is running.
    """
    scheduler = AsyncIOScheduler()

    trigger = CronTrigger(
        day_of_week=WEEKLY_REPORT_DAY,
        hour=WEEKLY_REPORT_HOUR,
        minute=WEEKLY_REPORT_MINUTE,
    )

    scheduler.add_job(
        _weekly_job,
        trigger=trigger,
        id="weekly_air_quality_report",
        name="Weekly Air Quality Report",
        replace_existing=True,
    )

    logger.info(
        "Weekly job scheduled: every %s at %02d:%02d.",
        WEEKLY_REPORT_DAY,
        WEEKLY_REPORT_HOUR,
        WEEKLY_REPORT_MINUTE,
    )
    return scheduler
