from app.providers.base import AIProvider
from app.providers.openai import OpenAIProvider
from app.config import Settings


# Provider Factory
class ProviderFactory:
    """Factory for creating AI provider instances."""

    _providers = {}

    @classmethod
    def get_provider(cls, provider_name: str) -> AIProvider:
        """Get or create provider instance (singleton pattern)."""
        if provider_name not in cls._providers:
            if provider_name == "openai":
                cls._providers[provider_name] = OpenAIProvider(Settings.OPENAI_API_KEY)
            else:
                raise ValueError(f"Unknown provider: {provider_name}")

        return cls._providers[provider_name]

    @classmethod
    async def close_all(cls):
        """Close all provider clients."""
        for provider in cls._providers.values():
            await provider.close()
