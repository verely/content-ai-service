# API endpoint handlers
# =============================================================================

import logging
from datetime import datetime
from fastapi import HTTPException
from app.models.schemas import CommentRequest, CommentResponse
from app.providers.factory import ProviderFactory

logger = logging.getLogger(__name__)


async def suggest_comment(request: CommentRequest) -> CommentResponse:
    """
    Generate AI-powered comment suggestions for a given post.

    - **text**: The post content to comment on
    - **provider**: AI provider ("claude" or "openai")
    - **num_suggestions**: Number of suggestions to generate (1-5)
    """
    start_time = datetime.now()

    logger.info(
        f"Request received - Provider: {request.provider}, Text length: {len(request.text)}"
    )

    try:
        provider = ProviderFactory.get_provider(request.provider)

        result = await provider.generate_comments(request.text, request.num_suggestions)

        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return CommentResponse(
            suggestions=result["suggestions"],
            provider=request.provider,
            model=result["model"],
            processing_time_ms=round(processing_time, 2),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in suggest_comment: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


async def health_check():
    """Health check endpoint."""
    from app.config import settings

    return {
        "status": "healthy",
        "providers": {
            "openai": "configured" if settings.OPENAI_API_KEY else "not configured",
        },
        "timestamp": datetime.now().isoformat(),
    }
