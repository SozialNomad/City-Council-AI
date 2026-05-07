"""
Search Agent — processes web search results to provide a curated list
of headlines with links.
"""

from agents.base import BaseLLMAgent

class SearcherAgent(BaseLLMAgent):
    """Formats web search results into a clean list of headlines and links."""

    DISPLAY_NAME: str = "Searcher Agent"
    ICON: str = "🌐"

    SYSTEM_PROMPT: str = (
        "You are a News Curator specialized in local sustainability and the environment.\n\n"
        "STRICT RESPONSE FORMAT (FOLLOW EXACTLY):\n\n"
        "*🌐 LATEST ENVIRONMENTAL NEWS IN [CITY NAME]*\n\n"
        "- [Headline 1](Link 1)\n"
        "- [Headline 2](Link 2)\n"
        "- [Headline 3](Link 3)\n\n"
        "_(Note: Only include headlines actually related to sustainability or the environment in this specific city. If no results match, say so politely.)_"
    )
