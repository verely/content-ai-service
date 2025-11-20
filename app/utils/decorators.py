from functools import wraps
from typing import Callable, Awaitable
import httpx
import json
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)


# Decorator for AI API error handling
def handle_ai_errors(provider_name: str):
    """Decorator to handle common AI API errors."""

    def decorator(
        func: Callable[..., Awaitable[dict]],
    ) -> Callable[..., Awaitable[dict]]:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> dict:
            try:
                return await func(*args, **kwargs)
            except httpx.TimeoutException as e:
                logger.error(f"{provider_name} API timeout: {e}")
                raise HTTPException(
                    status_code=504, detail=f"{provider_name} service timeout"
                )
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"{provider_name} API HTTP error: {e.response.status_code} - {e.response.text}"
                )
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"{provider_name} service error",
                )
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse {provider_name} response: {e}")
                raise HTTPException(
                    status_code=500, detail="Invalid AI response format"
                )
            except ValueError as e:
                logger.error(f"{provider_name} response validation error: {e}")
                raise HTTPException(status_code=500, detail=str(e))
            except Exception as e:
                logger.error(
                    f"{provider_name} API unexpected error: {e}", exc_info=True
                )
                raise HTTPException(status_code=500, detail="Internal server error")

        return wrapper

    return decorator
