"""
Air Quality API client — fetches current pollution data from the
World Air Quality Index (WAQI) public API.

API docs: https://aqicn.org/json-api/doc/
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

import httpx

from config import AIR_QUALITY_API_KEY, AIR_QUALITY_LOCATION, WAQI_BASE_URL

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AirQualityData:
    """Snapshot of key pollution metrics for a location."""

    location: str
    aqi: int
    pm25: float
    pm10: float
    timestamp: str  # ISO-8601

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> AirQualityData:
        return cls(**data)


async def fetch_air_quality(
    location: str | None = None,
) -> AirQualityData:
    """Fetch current air quality from WAQI for *location*.

    Returns an :class:`AirQualityData` dataclass.
    Raises ``httpx.HTTPStatusError`` or ``ValueError`` on failure.
    """
    loc = location or AIR_QUALITY_LOCATION
    url = f"{WAQI_BASE_URL}/feed/{loc}/"
    params = {"token": AIR_QUALITY_API_KEY}

    logger.info("Fetching air quality for '%s' …", loc)

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()

    payload = resp.json()
    if payload.get("status") != "ok":
        raise ValueError(f"WAQI API error: {payload.get('data', payload)}")

    data = payload["data"]
    iaqi = data.get("iaqi", {})

    return AirQualityData(
        location=loc,
        aqi=int(data.get("aqi", 0)),
        pm25=float(iaqi.get("pm25", {}).get("v", 0.0)),
        pm10=float(iaqi.get("pm10", {}).get("v", 0.0)),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
