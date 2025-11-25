# AI Comment Suggester

A FastAPI backend service that generates AI-powered comment suggestions for social media posts using OpenAI.

## Architecture

**Service Design**
- Single-purpose REST API for generating AI comments
- Stateless and independently deployable
- Simple HTTP interface that can be consumed by any server-side application

**Technical Highlights**
- **Async architecture**: Non-blocking I/O with connection pooling (HTTPX)
- **Clean modular structure**: Layered design with clear separation of concerns
- **Provider abstraction**: Easy to extend with additional AI models (Claude, Gemini, etc.)
- **Production-oriented**: Error handling, logging, timeouts, fallback behavior

## 🛠️ Tech Stack

- **Framework**: FastAPI (async Python web framework)
- **HTTP Client**: HTTPX
- **Validation**: Pydantic v2
- **AI Provider**: OpenAI API
- **Deployment**: Render (with health checks)

The project is deployed on Render.
API documentation is available at:

- **Swagger UI**: https://ai-comment-service.onrender.com/docs
- **ReDoc**: https://ai-comment-service.onrender.com/redoc
