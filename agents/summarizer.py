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
        "Summarize the provided utilitarian and environmental analyses. "
        "Highlight key trade-offs and provide a single concluding thought. "
        "Your response must be extremely concise and short. "
        "Do not generate new arguments."
    )
