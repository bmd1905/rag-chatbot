.PHONY: help install test test-cov lint pre-commit commit type-check coverage clean hello-world

help:
	@echo "Available targets:"
	@echo "  install       - Install dependencies (uv sync)"
	@echo "  test          - Run all tests"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  type-check    - Run mypy type checking"
	@echo "  lint          - Run Ruff linting and formatting (auto-fixes)"
	@echo "  pre-commit    - Run all pre-commit hooks"
	@echo "  commit        - Create a conventional commit"
	@echo "  coverage      - Display coverage report (requires test-cov first)"
	@echo "  clean         - Remove generated files and caches"
	@echo "  hello-world   - Run hello world example"

install:
	uv sync

test:
	uv run pytest test/

test-cov:
	uv run pytest test/ --cov=backend --cov-report=term --cov-report=xml --cov-report=html

type-check:
	uv run mypy backend/

lint:
	uv run ruff check --fix .
	uv run ruff format

pre-commit:
	uv run pre-commit run --all-files

commit:
	uv run cz commit

coverage: test-cov
	@python -m http.server 8000 --directory htmlcov > /dev/null 2>&1 & \
	echo "Coverage report opened at http://localhost:8000"; \
	sleep 1

clean:
	rm -rf .pytest_cache .coverage htmlcov coverage.xml build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

hello-world:
	uv run python backend/hello_world.py
