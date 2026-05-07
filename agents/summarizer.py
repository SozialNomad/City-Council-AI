"""
Summarizer Agent — synthesises utilitarian and environmental
analyses into a balanced comparison.
"""

from agents.base import BaseLLMAgent


class SummarizerAgent(BaseLLMAgent):
    """Merges two viewpoints into a concise, balanced summary."""

    DISPLAY_NAME: str = "Synthesis"
    ICON: str = "📊"

    SYSTEM_PROMPT: str = (
        "You are an objective Synthesizer. "
        "You will receive two analyses of a situation: one utilitarian and one environmental. "
        "Your task is to briefly summarize both viewpoints, highlight the primary trade-offs, "
        "and provide a single concluding thought. "
        "Do not generate new arguments; only synthesize the provided text."
    )
