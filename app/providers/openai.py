import logging
from app.providers.base import AIProvider
from app.utils.decorators import handle_ai_errors
from app.config import Settings

logger = logging.getLogger(__name__)


class OpenAIProvider(AIProvider):
    """OpenAI AI provider."""

    @handle_ai_errors("OpenAI")
    async def generate_comments(self, text: str, num_suggestions: int) -> dict:
        logger.info(f"Calling OpenAI API for {num_suggestions} suggestions")

        response = await self.client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": Settings.SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": self._build_prompt(text, num_suggestions),
                    },
                ],
                "temperature": 0.8,
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]
        suggestions = self._parse_response(content)

        logger.info(f"OpenAI API success: {len(suggestions)} suggestions generated")

        return {"suggestions": suggestions, "model": data["model"]}
