# Tech Stack

## Language & Runtime
- Python 3.11+

## Package Management
- uv (Astral's fast Python package manager)

## Backend Framework
- FastAPI with Uvicorn ASGI server
- Pydantic for request/response schemas

## AI/ML
- OpenAI API (gpt-4o-mini model)
- ChromaDB for vector storage and semantic search

## Frontend
- Vanilla HTML/CSS/JavaScript (no framework)
- Single-file SPA served by FastAPI

## Development Tools
- Ruff for linting and formatting
- Pre-commit hooks for code quality
- Commitizen for conventional commits
- Pytest for testing with coverage support

## Common Commands

```bash
# Install dependencies
uv sync

# Run development server
make run
# or: uv run uvicorn backend.main:app --reload

# Run tests
make mock-test
# or: uv run pytest

# Run tests with coverage
uv run pytest --cov=backend --cov-report=xml

# Lint and format code
make lint
# or: uv run ruff check --fix . && uv run ruff format

# Run pre-commit hooks
make pre-commit

# Create conventional commit
make commit
```

## Environment Variables
- `OPENAI_API_KEY` - Required for LLM calls (see `.env.example`)
