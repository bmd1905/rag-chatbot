.PHONY: hello-world test lint pre-commit commit

hello-world:
	uv run python backend/hello_world.py

mock-test:
	uv run pytest

lint:
	uv run ruff check --fix
	uv run ruff format

pre-commit:
	uv run pre-commit run --all-files

commit:
	uv run cz commit
