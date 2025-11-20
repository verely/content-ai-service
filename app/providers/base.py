import httpx
import json
from abc import ABC, abstractmethod
from typing import List
from app.config import Settings


# Abstract base class for AI providers
class AIProvider(ABC):
    """Base class for AI providers."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError(f"{self.__class__.__name__} API key not configured")
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            timeout=Settings.TIMEOUT_CONFIG, limits=Settings.LIMITS
        )

    @abstractmethod
    async def generate_comments(self, text: str, num_suggestions: int) -> dict:
        """Generate comment suggestions. Returns dict with 'suggestions' and 'model'."""
        pass

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    def _build_prompt(self, text: str, num_suggestions: int) -> str:
        """Build user prompt."""
        return f"Suggest {num_suggestions} friendly, short comments for a social media post based on this text: {text}."

    def _parse_response(self, content: str) -> List[str]:
        """Parse JSON response and extract comments."""
        parsed = json.loads(content.strip())

        if isinstance(parsed, dict) and "comments" in parsed:
            suggestions = parsed["comments"]
        elif isinstance(parsed, list):
            suggestions = parsed
        else:
            raise ValueError(f"Unexpected response format: {parsed}")

        if not isinstance(suggestions, list) or not suggestions:
            raise ValueError("No valid comments array found in response")

        return suggestions
