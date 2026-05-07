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


import asyncio
from typing import AsyncGenerator

async def run_comparison(user_message: str) -> AsyncGenerator[dict[str, str], None]:
    """Execute the comparison pipeline and yield results as they become ready.

    Utilitarian and Green agents run in parallel. The Summarizer runs
    after both are complete.
    """
    utilitarian, green, summarizer = _get_agents()

    logger.info("Starting parallel comparison pipeline …")

    # 1. Run Utilitarian and Green agents concurrently
    # We use tasks so we can wait for them and handle results
    util_task = asyncio.create_task(utilitarian.generate(user_message))
    green_task = asyncio.create_task(green.generate(user_message))

    # Wait for both to finish (we could yield them as they finish using as_completed,
    # but to maintain a consistent order [Util -> Green -> Summary], we'll just wait)
    # Actually, the user wants them as they are ready.
    
    pending = {util_task, green_task}
    results_map = {}

    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task == util_task:
                output = task.result()
                results_map["utilitarian"] = output
                logger.info("Utilitarian analysis complete.")
                yield {
                    "name": utilitarian.DISPLAY_NAME,
                    "icon": utilitarian.ICON,
                    "content": output,
                }
            elif task == green_task:
                output = task.result()
                results_map["green"] = output
                logger.info("Green analysis complete.")
                yield {
                    "name": green.DISPLAY_NAME,
                    "icon": green.ICON,
                    "content": output,
                }

    # 2. Run Summarizer (depends on previous two)
    combined_input = textwrap.dedent(f"""\
        User's original message:
        {user_message}

        --- Utilitarian Analysis ---
        {results_map['utilitarian']}

        --- Environmental Analysis ---
        {results_map['green']}
    """)

    summary = await summarizer.generate(combined_input)
    logger.info("Summarizer complete — pipeline finished.")

    yield {
        "name": summarizer.DISPLAY_NAME,
        "icon": summarizer.ICON,
        "content": summary,
    }
