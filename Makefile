.PHONY: hello-world test lint pre-commit commit run

hello-world:
	uv run python backend/hello_world.py

run:
	uv run uvicorn backend.main:app --reload

mock-test:
	uv run pytest

lint:
	uv run ruff check --fix .
	uv run ruff format

pre-commit:
	uv run pre-commit run --all-files

commit:
	uv run cz commit
