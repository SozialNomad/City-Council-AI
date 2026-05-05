"""
Base LLM Agent — isolated wrapper for OpenAI.

All domain-specific agents inherit from this class. They only need
to supply a system prompt; the API plumbing lives entirely here.
"""

from __future__ import annotations

import logging
from openai import AsyncOpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)


class BaseLLMAgent:
    """Thin async wrapper around the OpenAI generative API.

    Subclasses set ``SYSTEM_PROMPT`` as a class variable and call
    ``await self.generate(user_input)`` to get a response.
    """

    SYSTEM_PROMPT: str = ""

    def __init__(self, model: str | None = None) -> None:
        self._model = model or OPENAI_MODEL
        self._client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate(self, user_input: str) -> str:
        """Send *user_input* to OpenAI and return the model's text response.

        The system prompt is injected automatically.
        """
        logger.info(
            "Agent %s generating response (model=%s) …",
            self.__class__.__name__,
            self._model,
        )

        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        text: str = response.choices[0].message.content or ""
        logger.debug("Agent %s response length: %d chars", self.__class__.__name__, len(text))
        return text
