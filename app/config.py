import os
import httpx
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # HTTP Client Configuration
    TIMEOUT_CONFIG = httpx.Timeout(connect=10.0, read=90.0, write=10.0, pool=10.0)

    # Shared connection pool limits
    LIMITS = httpx.Limits(
        max_keepalive_connections=20, max_connections=100, keepalive_expiry=30.0
    )

    # AI Configuration
    SYSTEM_PROMPT = """You are a helpful assistant that generates engaging social media comments.
    Always respond with a JSON object following this exact structure:
    {
    "comments": ["comment 1", "comment 2", "comment 3"]
    }"""


settings = Settings()
