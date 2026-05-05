"""
Workflow 1 — Multi-Agent Comparator.

Runs three agents *sequentially* against a user message:
    Utilitarian → Green → Summarizer
and returns the Summarizer's output.
"""

from __future__ import annotations

import logging
import textwrap

from agents.utilitarian import UtilitarianAgent
from agents.green import GreenAgent
from agents.summarizer import SummarizerAgent

logger = logging.getLogger(__name__)

# Lazily instantiated singletons (created on first call).
_utilitarian: UtilitarianAgent | None = None
_green: GreenAgent | None = None
_summarizer: SummarizerAgent | None = None


def _get_agents() -> tuple[UtilitarianAgent, GreenAgent, SummarizerAgent]:
    global _utilitarian, _green, _summarizer
    if _utilitarian is None:
        _utilitarian = UtilitarianAgent()
    if _green is None:
        _green = GreenAgent()
    if _summarizer is None:
        _summarizer = SummarizerAgent()
    return _utilitarian, _green, _summarizer


async def run_comparison(user_message: str) -> str:
    """Execute the full comparison pipeline and return the summary text.

    Steps (sequential — each depends on the previous):
        1. Utilitarian analysis
        2. Green / Environmental analysis
        3. Summarizer synthesises both analyses
    """
    utilitarian, green, summarizer = _get_agents()

    logger.info("Starting comparison pipeline …")

    # Step 1 — Utilitarian perspective
    utilitarian_output = await utilitarian.generate(user_message)
    logger.info("Utilitarian analysis complete.")

    # Step 2 — Environmental perspective
    green_output = await green.generate(user_message)
    logger.info("Green analysis complete.")

    # Step 3 — Synthesis
    combined_input = textwrap.dedent(f"""\
        User's original message:
        {user_message}

        --- Utilitarian Analysis ---
        {utilitarian_output}

        --- Environmental Analysis ---
        {green_output}
    """)

    summary = await summarizer.generate(combined_input)
    logger.info("Summarizer complete — pipeline finished.")

    return summary
