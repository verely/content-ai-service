from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class CommentRequest(BaseModel):
    """Request model for comment suggestions."""

    text: str = Field(..., description="The post/content to comment on", min_length=1)
    provider: Literal["claude", "openai"] = Field(
        default="openai", description="AI provider to use"
    )
    num_suggestions: int = Field(
        default=3, ge=1, le=5, description="Number of comment suggestions (1-5)"
    )
    


class CommentResponse(BaseModel):
    """Response model with generated comments."""

    suggestions: List[str]
    provider: str
    model: str
    processing_time_ms: float


class ErrorResponse(BaseModel):
    """Error response model."""

    error: str
    details: Optional[str] = None
    timestamp: str


class CommentSchema(BaseModel):
    """Expected schema from AI providers."""

    comments: List[str]
