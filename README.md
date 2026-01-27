# RAG Chatbot

[![build status](https://github.com/bmd1905/rag-chatbot/actions/workflows/test.yml/badge.svg)](https://github.com/bmd1905/rag-chatbot/actions/workflows/test.yml) [![codecov](https://codecov.io/github/bmd1905/rag-chatbot/graph/badge.svg?token=5MTJSYWD05)](https://codecov.io/github/bmd1905/rag-chatbot) [![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fbmd1905%2Frag-chatbot%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://github.com/bmd1905/rag-chatbot/blob/main/pyproject.toml)
[![GitHub License](https://img.shields.io/github/license/bmd1905/rag-chatbot)](https://github.com/bmd1905/rag-chatbot/blob/main/LICENSE)

## Overview

A Python chatbot that uses Retrieval-Augmented Generation (RAG) to answer questions about given contexts. This project demonstrates modern Python development practices with strict code quality standards, comprehensive testing, and type safety.

## Features

- **RAG Architecture**: Retrieval-Augmented Generation for context-aware responses
- **Type Safe**: Full type hints with mypy static type checking
- **Well Tested**: Comprehensive test suite with coverage reporting
- **Code Quality**: Strict Ruff linting with multiple rule sets
- **Pre-commit Hooks**: Automated code quality checks on commit
- **Modern Tooling**: Uses `uv` for fast, reliable dependency management

## Quick Start

### Prerequisites

- Python 3.11 or 3.12
- [uv](https://docs.astral.sh/uv/getting-started/installation/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/bmd1905/rag-chatbot.git
cd rag-chatbot

# Install dependencies
uv sync

# Install pre-commit hooks (optional but recommended)
uv run pre-commit install
```

### Running Tests

```bash
# Run all tests
make test

# Run tests with coverage report
make test-cov

# Run a specific test file
uv run pytest test/backend/test_hello_world.py -v
```

### Code Quality

```bash
# Lint and format code (auto-fixes issues)
make lint

# Type check with mypy
make type-check

# Run all pre-commit hooks
make pre-commit
```

### Available Commands

Run `make help` to see all available commands:

```
install       - Install dependencies (uv sync)
test          - Run all tests
test-cov      - Run tests with coverage report
type-check    - Run mypy type checking
lint          - Run Ruff linting and formatting (auto-fixes)
pre-commit    - Run all pre-commit hooks
commit        - Create a conventional commit
coverage      - Display coverage report (requires test-cov first)
clean         - Remove generated files and caches
hello-world   - Run hello world example
```

## Project Structure

```
rag-chatbot/
├── backend/                 # Core backend module
│   ├── __init__.py
│   └── hello_world.py       # Example module
├── test/                    # Test suite
│   ├── __init__.py
│   └── backend/
│       ├── __init__.py
│       └── test_hello_world.py
├── pyproject.toml           # Project configuration
├── Makefile                 # Development commands
├── README.md                # This file
├── CLAUDE.md                # Claude Code guidance
└── LICENSE                  # MIT License
```

## Development

### Setting Up Your Environment

1. Install dependencies: `make install`
2. Install pre-commit hooks: `uv run pre-commit install`
3. Verify setup: `make test && make lint`

### Making Changes

Before committing, ensure:

1. Code passes all tests: `make test`
2. Code is properly formatted: `make lint`
3. Type checking passes: `make type-check`
4. Pre-commit hooks pass: `make pre-commit`

Or run all checks at once before committing:

```bash
make test && make type-check && make lint && make pre-commit
```

### Creating a Commit

Use commitizen for conventional commits:

```bash
make commit
```

This ensures commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Code Quality Standards

### Linting and Formatting

The project uses [Ruff](https://docs.astral.sh/ruff/) with the following rules:

- **F** - Pyflakes (logical errors)
- **I** - isort (import sorting)
- **TCH** - Type-checking imports
- **UP** - pyupgrade (modern syntax)
- **PLC** - Pylint conventions
- **D** - pydocstyle (docstrings)
- **E** - pycodestyle (PEP8 errors)
- **W** - pycodestyle (warnings)
- **N** - pep8-naming (naming conventions)
- **S** - flake8-bandit (security issues)

Line length: 120 characters

### Type Checking

All code is type-checked with [mypy](https://www.mypy-lang.org/) using strict mode options:

- `disallow_incomplete_defs`: Functions must have complete type information
- `check_untyped_defs`: Check functions without type hints
- `no_implicit_optional`: Explicit Optional types required
- `strict_equality`: Strict equality checks

### Testing

Tests use [pytest](https://pytest.org/) with:

- `pytest-cov`: Coverage reporting
- `pytest-asyncio`: Async test support
- `pytest-env`: Environment variable management

Coverage reports are generated in HTML format in `htmlcov/` directory.

## Pre-commit Hooks

Pre-commit hooks automatically run before each commit and validate:

- File sizes and syntax (YAML, JSON, TOML)
- Merge conflict markers
- Trailing whitespace
- Private key detection
- Ruff linting and formatting
- Commit message format (commitizen)

## Contributing

Please follow these guidelines:

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass: `make test`
4. Run linting: `make lint`
5. Run type checking: `make type-check`
6. Use conventional commits: `make commit`
7. Submit a pull request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.
