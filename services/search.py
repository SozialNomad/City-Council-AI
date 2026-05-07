from __future__ import annotations
import logging
from ddgs import DDGS

logger = logging.getLogger(__name__)

def perform_search(query: str, max_results: int = 5) -> list[dict[str, str]]:
    """Perform a news search using DuckDuckGo and return a list of results.
    
    Each result is a dict with 'title', 'href', and 'body'.
    """
    logger.info("Performing news search for: %s", query)
    results = []
    try:
        with DDGS() as ddgs:
            # Note: news() returns a generator with 'title', 'url', 'body'
            ddgs_results = ddgs.news(query, max_results=max_results)
            for r in ddgs_results:
                results.append({
                    "title": r.get("title", ""),
                    "href": r.get("url", ""),  # news() uses 'url' instead of 'href'
                    "body": r.get("body", "")
                })
    except Exception as e:
        logger.error("DDGS news search failed: %s", e)
    
    return results
