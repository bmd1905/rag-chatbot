.PHONY:  test lint pre-commit commit
lint:
	uv run ruff check --fix
	uv run ruff format

pre-commit:
	uv run pre-commit run --all-files

commit:
	uv run cz commit
