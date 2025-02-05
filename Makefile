hello-world:
	uv run python backend/hello_world.py

lint:
	uv run ruff check --fix
	uv run ruff format

pre-commit:
	uv run pre-commit run --all-files
