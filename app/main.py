# uvicorn app.main:app --reload
# http://127.0.0.1:8000/docs
# FastAPI application initialization
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.utils.log_config import setup_logging
from app.models.schemas import CommentRequest, CommentResponse, ErrorResponse
from app.api import routes
from app.providers.factory import ProviderFactory


setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Code before yield runs on startup.
    Code after yield runs on shutdown.
    """
    # Startup
    logger.info("Starting AI Comment Service...")

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down, closing provider connections...")
    await ProviderFactory.close_all()


# Create FastAPI app with lifespan
app = FastAPI(
    title="AI Comment Suggester",
    version="1.0.0",
    description="Generate AI-powered comment suggestions using OpenAI",
    lifespan=lifespan,
)

# Register routes


@app.post("/suggest-comment", response_model=CommentResponse)
async def suggest_comment_endpoint(request: CommentRequest):
    return await routes.suggest_comment(request)


@app.get("/health")
async def health_check_endpoint():
    return await routes.health_check()


# Exception handler


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom error handler for better logging and response format."""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail, timestamp=datetime.now().isoformat()
        ).model_dump()(),
    )


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
