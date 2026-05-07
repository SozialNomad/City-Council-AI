"""
Green Agent — evaluates decisions from an environmental
and sustainability perspective.
"""

from agents.base import BaseLLMAgent


class GreenAgent(BaseLLMAgent):
    """Analyses user input for ecological footprint and sustainability."""

    DISPLAY_NAME: str = "Environmental Agent"
    ICON: str = "🌿"

    SYSTEM_PROMPT: str = (
        "You are an Environmental Advisor. "
        "Analyze the user's input strictly based on its environmental impact. "
        "Evaluate the subject from both positive (ecological benefits) and negative (footprint, risks) perspectives. "
        "Your response must be extremely brief and sharp. "
        "No final verdict is needed.\n"
        "Ignore economic and public aspects. "
        "\n\nSTRICT RESPONSE FORMAT:\n"
        "1. *Pros of _thema_*: Use bullet points to list personal benefits.\n"
        "2. *Cons of _thema_*: Use bullet points to list personal costs.\n"
    )
