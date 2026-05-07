"""
Centralized configuration module.

Loads environment variables from a .env file and exposes them as
typed module-level constants. All other modules should import from
here instead of calling os.getenv() directly.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from project root
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(_PROJECT_ROOT / ".env")

# ---------------------------------------------------------------------------
# Telegram
# ---------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN: str = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID: str = os.environ["TELEGRAM_CHAT_ID"]

# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------
OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# ---------------------------------------------------------------------------
# Air Quality (WAQI)
# ---------------------------------------------------------------------------
AIR_QUALITY_API_KEY: str = os.environ["AIR_QUALITY_API_KEY"]
AIR_QUALITY_LOCATION: str = os.getenv("AIR_QUALITY_LOCATION", "würzburg")
WAQI_BASE_URL: str = "https://api.waqi.info"

# ---------------------------------------------------------------------------
# Local storage
# ---------------------------------------------------------------------------
DATA_DIR: Path = _PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)
AIR_QUALITY_HISTORY_FILE: Path = DATA_DIR / "air_quality_history.json"
