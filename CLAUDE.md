# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RAG Chatbot is a Python project that implements a chatbot using Retrieval-Augmented Generation (RAG) models to answer questions about given contexts. The project uses modern Python tooling with `uv` as the package manager, `FastAPI` for API infrastructure, and follows strict code quality standards with Ruff linting and pre-commit hooks.

## Core Technology Stack

- **Python**: 3.11+ (tested on 3.11, 3.12)
- **Package Manager**: `uv` (required for all package management and test execution)
- **API Framework**: FastAPI
- **Code Quality**: Ruff (linting and formatting)
- **Testing**: pytest with coverage tracking
- **Commit Standards**: commitizen

## Development Commands

All commands use `uv run` to execute in the project environment. Install dependencies first with `uv sync`.

### Common Development Tasks

```bash
# Install dependencies
uv sync

# Run all tests
uv run pytest

# Run a specific test file
uv run pytest test/backend/mock_test.py

# Run tests with coverage report (XML format for CI)
uv run pytest --cov=backend --cov-report=xml

# Run tests with verbose output
uv run pytest -v

# Lint and format code (fixes issues automatically)
make lint
# OR manually:
uv run ruff check --fix .
uv run ruff format

# Run pre-commit hooks on all files
uv run pre-commit install  # Install hooks (do once per dev environment)
uv run pre-commit run --all-files

# Create a conventional commit
uv run cz commit

# Run the hello_world example
make hello-world
```

## Project Structure

```
backend/           # Main application code
test/backend/      # Test files (mirrors backend structure)
notebooks/         # Jupyter notebooks for POC and exploration
pyproject.toml     # Project metadata and tool configuration
Makefile           # Common development targets
```

## Code Quality Standards

### Ruff Configuration

The project uses Ruff with these key settings (in `pyproject.toml`):
- **Line length**: 120 characters
- **Python target**: 3.11+
- **Selected rules**:
  - `F` (Pyflakes - logical errors)
  - `I` (isort - import sorting)
  - `TCH` (Type-checking imports)
  - `UP` (pyupgrade - modern syntax)
  - `PLC` (Pylint conventions)
- **isort config**: Uses first-party imports under `backend` namespace
- **Per-file ignores**: Notebooks and `__init__.py` have relaxed rules

### Pre-commit Hooks

Pre-commit hooks run automatically before commits and validate:
- File sizes, TOML/JSON/YAML syntax
- Merge conflicts and private keys
- Trailing whitespace
- Ruff linting and formatting
- Commitizen commit message format

## Testing

Tests are located in `test/` and mirror the backend structure. The test framework is pytest with the following plugins:
- `pytest-cov`: Coverage reporting
- `pytest-env`: Environment variable management
- `pytest-asyncio`: Async test support

Run tests before pushing:
```bash
uv run pytest test/ -v --cov=backend --cov-report=xml
```

The CI pipeline tests on Python 3.11 and 3.12, uploading coverage to Codecov.

## Import Organization

The project uses `backend` as the first-party module namespace. When adding new code:
- Internal imports should use `from backend.module import ...`
- Imports are split into standard library, third-party, and first-party sections
- Use `combine-as-imports` and `force-single-line` isort settings (already configured)
