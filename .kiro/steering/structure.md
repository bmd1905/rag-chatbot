# Project Structure

```
.
├── backend/           # Python backend code
│   ├── main.py        # FastAPI app, routes, middleware
│   ├── agent.py       # RAG pipeline: retrieval + LLM generation
│   ├── schemas.py     # Pydantic request/response models
│   └── hello_world.py # Example/utility module
├── frontend/          # Static web assets
│   └── index.html     # Single-page chat interface
├── test/              # Test suite
│   └── backend/       # Backend unit tests
├── notebooks/         # Jupyter notebooks for experimentation
├── pyproject.toml     # Project config, dependencies, tool settings
├── Makefile           # Common development commands
└── uv.lock            # Locked dependency versions
```

## Conventions

- Backend modules live in `backend/` as flat Python files
- Tests mirror source structure under `test/`
- Pydantic models for all API contracts in `schemas.py`
- Environment config via `.env` file (dotenv loaded in main.py)
- Ruff handles both linting and import sorting (isort rules)
- Line length: 120 characters
- First-party imports: `backend`
