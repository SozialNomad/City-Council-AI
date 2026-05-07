"""
Local JSON storage for air quality history.

Persists a single JSON object representing last week's data so
that Workflow 2 can compute week-over-week deltas.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from config import AIR_QUALITY_HISTORY_FILE, SETTINGS_FILE

logger = logging.getLogger(__name__)


def load_previous_data(path: Path | None = None) -> dict | None:
    """Read the last saved air quality snapshot from disk.

    Returns ``None`` if the file does not exist or is empty/corrupt.
    """
    filepath = path or AIR_QUALITY_HISTORY_FILE
    if not filepath.exists():
        logger.info("No previous air quality data found at %s.", filepath)
        return None

    try:
        with filepath.open("r", encoding="utf-8") as fh:
            data: dict = json.load(fh)
        logger.info("Loaded previous data from %s.", filepath)
        return data
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read %s: %s", filepath, exc)
        return None


def save_current_data(data: dict, path: Path | None = None) -> None:
    """Persist *data* (the current week's snapshot) to disk."""
    filepath = path or AIR_QUALITY_HISTORY_FILE
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)

    logger.info("Saved current air quality data to %s.", filepath)


def load_settings() -> dict:
    """Read global settings (e.g. current city) from disk."""
    if not SETTINGS_FILE.exists():
        return {}

    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Failed to read settings: %s", exc)
        return {}


def save_settings(settings: dict) -> None:
    """Persist settings to disk."""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SETTINGS_FILE.open("w", encoding="utf-8") as fh:
        json.dump(settings, fh, indent=2, ensure_ascii=False)
    logger.info("Settings saved to %s.", SETTINGS_FILE)
