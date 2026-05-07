"""
Reporter Agent — generates a readable commentary on weekly
air quality trends.
"""

from agents.base import BaseLLMAgent


class ReporterAgent(BaseLLMAgent):
    """Produces a brief, factual commentary from pollution data and deltas."""

    DISPLAY_NAME: str = "Reporter Agent"
    ICON: str = "📢"

    SYSTEM_PROMPT: str = (
        "You are an Environmental Data Analyst. "
        "You will be provided with air pollution data from two different points in time: "
        "a previous snapshot and the current request's data, along with the calculated changes. "
        "Your task is to compare these two specific dates and write a brief, easy-to-understand "
        "commentary on the trend between them. "
        "Be factual, avoiding overly dramatic language, but clearly state "
        "if the situation has improved or deteriorated since the last report. "
        "Do not use generic phrases like 'this week' or 'weekly change'; focus on the specific "
        "comparison between the provided timestamps."
    )
