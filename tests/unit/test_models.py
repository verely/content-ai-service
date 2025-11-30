import pytest
from pydantic import ValidationError
from app.models.schemas import CommentRequest, CommentResponse


class TestCommentRequest:
    """Test CommentRequest model validation."""

    def test_valid_request_with_defaults(self):
        """Test valid request with default values."""
        request = CommentRequest(text="Hello world")
        assert request.text == "Hello world"
        assert request.provider == "openai"
        assert request.num_suggestions == 3

    def test_valid_request_with_all_fields(self):
        """Test valid request with all fields specified."""
        request = CommentRequest(text="Test post", provider="openai", num_suggestions=5)
        assert request.text == "Test post"
        assert request.provider == "openai"
        assert request.num_suggestions == 5

    def test_empty_text_fails(self):
        """Test that empty text is rejected."""
        with pytest.raises(ValidationError):
            CommentRequest(text="")

    def test_invalid_provider_fails(self):
        """Test that invalid provider is rejected."""
        with pytest.raises(ValidationError):
            CommentRequest(text="Test", provider="gemini")


class TestCommentResponse:
    """Test CommentResponse model."""

    def test_valid_response(self):
        """Test valid response creation."""
        response = CommentResponse(
            suggestions=["Comment 1", "Comment 2"],
            provider="claude",
            model="claude-sonnet-4",
            processing_time_ms=1234.56,
        )
        assert len(response.suggestions) == 2
        assert response.provider == "claude"
        assert response.processing_time_ms == 1234.56
