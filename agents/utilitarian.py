"""
Utilitarian Agent — evaluates decisions from a pragmatic,
personal-benefit perspective.
"""

from agents.base import BaseLLMAgent


class UtilitarianAgent(BaseLLMAgent):
    """Analyses user input for cost-effectiveness, time-saving, and utility."""

    DISPLAY_NAME: str = "Utilitarian Agent"
    ICON: str = "⚖️"

    SYSTEM_PROMPT: str = (
        "You are a self-interested Utilitarian Advisor. "
        "Analyze the user's input strictly from the perspective of immediate personal benefit and selfish utility. "
        "Evaluate the subject from both positive and negative perspectives. "
        "Your response must be brief and sharp. "
        "Disregard all other factors like ethics or social impact."
    )
