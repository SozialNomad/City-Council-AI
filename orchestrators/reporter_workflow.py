"""
Workflow 2 — On-demand Air Quality Summary.

Fetches current pollution data, compares to previous snapshot,
generates an LLM commentary, and sends it to Telegram.
"""

from __future__ import annotations

import logging
import textwrap

from agents.reporter import ReporterAgent
from services.air_quality import AirQualityData, fetch_air_quality
from services.storage import load_previous_data, save_current_data, load_settings
from services.search import perform_search

logger = logging.getLogger(__name__)

_reporter: ReporterAgent | None = None


def _get_reporter() -> ReporterAgent:
    global _reporter
    if _reporter is None:
        _reporter = ReporterAgent()
    return _reporter


def _calculate_deltas(
    current: AirQualityData,
    previous: dict | None,
) -> dict[str, float | str]:
    """Return a dict of metric deltas (current − previous).

    If *previous* is ``None`` (first run), all deltas are marked ``"N/A"``.
    """
    if previous is None:
        return {"aqi": "N/A", "pm25": "N/A", "pm10": "N/A"}

    return {
        "aqi": current.aqi - int(previous.get("aqi", 0)),
        "pm25": round(current.pm25 - float(previous.get("pm25", 0.0)), 2),
        "pm10": round(current.pm10 - float(previous.get("pm10", 0.0)), 2),
    }


def _format_report_input(
    current: AirQualityData,
    previous: dict | None,
    deltas: dict,
    news: list[dict[str, str]] | None = None,
) -> str:
    """Build a structured text block for the Reporter agent."""
    prev_section = "No previous data available (first report)."
    if previous is not None:
        prev_section = textwrap.dedent(f"""\
            AQI:   {previous.get('aqi', 'N/A')}
            PM2.5: {previous.get('pm25', 'N/A')}
            PM10:  {previous.get('pm10', 'N/A')}
            Date:  {previous.get('timestamp', 'N/A')}""")

    news_section = "No relevant recent news found."
    if news:
        news_section = "\n".join([f"- {r['title']} | Source: {r['href']}" for r in news])

    return textwrap.dedent(f"""\
        Location: {current.location}

        --- Current Snapshot ---
        AQI:   {current.aqi}
        PM2.5: {current.pm25}
        PM10:  {current.pm10}
        Date:  {current.timestamp}

        --- Previous Snapshot ---
        {prev_section}

        --- Changes (Δ) ---
        AQI:   {deltas['aqi']}
        PM2.5: {deltas['pm25']}
        PM10:  {deltas['pm10']}

        --- Latest Local News ---
        {news_section}
    """)


async def run_report_workflow() -> str:
    """Execute the full air quality report pipeline.

    Returns the generated commentary text.
    """
    reporter = _get_reporter()

    logger.info("Starting report summary pipeline …")

    # 0. Get current city from settings
    settings = load_settings()
    current_city = settings.get("city")  # Falls back to None, then fetch_air_quality uses config default

    # 1. Fetch current data
    current_data = await fetch_air_quality(location=current_city)
    logger.info("Fetched current air quality for %s: AQI=%d", current_data.location, current_data.aqi)

    # 2. Load previous data
    previous_data = load_previous_data()

    # 3. Compute deltas - Skip comparison if city has changed
    if previous_data and previous_data.get("location") != current_data.location:
        logger.info("City changed from %s to %s. Skipping comparison.", 
                    previous_data.get("location"), current_data.location)
        previous_data = None

    deltas = _calculate_deltas(current_data, previous_data)
    logger.info("Deltas computed: %s", deltas)

    # 4. Fetch latest news for the city
    search_query = f'"{current_data.location}" sustainability environment "climate change"'
    news_results = perform_search(search_query, max_results=3)
    logger.info("Fetched %d news results for %s", len(news_results), current_data.location)

    # 5. Generate commentary
    report_input = _format_report_input(current_data, previous_data, deltas, news_results)
    commentary = await reporter.generate(report_input)
    logger.info("Reporter commentary generated.")

    # 5. Persist current data for next time
    save_current_data(current_data.to_dict())

    return commentary
