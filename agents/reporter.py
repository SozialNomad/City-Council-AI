"""
Reporter Agent — generates a readable commentary on weekly
air quality trends.
"""

from agents.base import BaseLLMAgent


class ReporterAgent(BaseLLMAgent):
    """Produces a brief, factual commentary from pollution data and deltas."""

    SYSTEM_PROMPT: str = (
        "You are an Environmental Data Analyst. "
        "You will be provided with this week's air pollution data, last week's data, "
        "and the calculated changes. "
        "Write a brief, easy-to-understand commentary on the trend. "
        "Be factual, avoiding overly dramatic language, but clearly state "
        "if the situation is improving or deteriorating."
    )
