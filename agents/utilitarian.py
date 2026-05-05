"""
Utilitarian Agent — evaluates decisions from a pragmatic,
personal-benefit perspective.
"""

from agents.base import BaseLLMAgent


class UtilitarianAgent(BaseLLMAgent):
    """Analyses user input for cost-effectiveness, time-saving, and utility."""

    SYSTEM_PROMPT: str = (
        "You are a highly pragmatic Utilitarian Advisor. "
        "Analyze the user's input strictly from the perspective of personal benefit, "
        "cost-effectiveness, time-saving, and practical utility. "
        "Ignore environmental concerns. "
        "Keep your analysis concise and structured."
    )
