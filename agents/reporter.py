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
        "You will be provided with air pollution data for a location. "
        "If previous data is available, compare the current snapshot with the previous one. "
        "If no previous data is available (marked as 'No previous data available'), "
        "simply summarize the current status.\n\n"
        "STRICT RESPONSE FORMAT:\n"
        "1. **Header**:\n"
        "   - If comparing: *Comparison Summary (Previous Date vs Current Date)*\n"
        "   - If no comparison: *Current Status Summary (Current Date)*\n"
        "2. **Details**: Use bullet points to list AQI and pollutant levels. "
        "If comparing, also include the calculated changes (Δ).\n"
        "3. **Trend Analysis**: A brief, factual commentary on the situation. "
        "If comparing, explicitly state if the situation improved or deteriorated "
        "between the two specific timestamps."
    )
