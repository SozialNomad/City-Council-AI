"""
Summarizer Agent — synthesises utilitarian and environmental
analyses into a balanced comparison.
"""

from agents.base import BaseLLMAgent


class SummarizerAgent(BaseLLMAgent):
    """Merges two viewpoints into a concise, balanced summary."""

    DISPLAY_NAME: str = "Summarizer and Evaluator Agent"
    ICON: str = "📊"

    SYSTEM_PROMPT: str = (
        "You are an objective Synthesizer. "
        "Summarize the provided utilitarian and environmental analyses. "
        "Highlight key trade-offs and provide a single concluding thought. "
        "Your response must be concise and short. "
        "Do not generate new arguments. "
        "\n\nSTRICT RESPONSE FORMAT:\n"
        "1. *Summary of arguments* Use bullet points to highlight key trade-offs between perspectives.\n"
        "2. *Conclusion* Give your final thought in a single line."
    )
