"""
Green Agent — evaluates decisions from an environmental
and sustainability perspective.
"""

from agents.base import BaseLLMAgent


class GreenAgent(BaseLLMAgent):
    """Analyses user input for ecological footprint and sustainability."""

    DISPLAY_NAME: str = "Environmental Advisor"
    ICON: str = "🌿"

    SYSTEM_PROMPT: str = (
        "You are an Environmental Advisor. "
        "Analyze the user's input strictly based on its environmental impact. "
        "Evaluate the subject from both positive (ecological benefits) and negative (footprint, risks) perspectives. "
        "Your response must be extremely brief and sharp. "
        "Ignore economic and public aspects."
    )
