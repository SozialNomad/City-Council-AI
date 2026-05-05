"""
Green Agent — main entry point.

Boots the Telegram bot and the weekly APScheduler on the same
asyncio event loop. Both run concurrently until interrupted.
"""

from __future__ import annotations

import logging

from config import TELEGRAM_CHAT_ID  # noqa: F401  — validates env early
from scheduler.weekly import create_scheduler, set_telegram_app
from services.telegram_bot import build_application

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Initialise and start all subsystems."""

    # 1. Build the Telegram bot application
    app = build_application()

    # 2. Create the weekly scheduler and give it access to the bot
    scheduler = create_scheduler()
    set_telegram_app(app)

    # 3. Register lifecycle hooks so the scheduler starts/stops with the bot
    async def _post_init(application) -> None:  # noqa: ANN001
        scheduler.start()
        logger.info("Scheduler started.")

    async def _post_shutdown(application) -> None:  # noqa: ANN001
        scheduler.shutdown(wait=False)
        logger.info("Scheduler shut down.")

    app.post_init = _post_init
    app.post_shutdown = _post_shutdown

    # 4. Start polling (blocking — runs until Ctrl+C)
    logger.info("Starting Green Agent bot …")
    app.run_polling()


if __name__ == "__main__":
    main()
