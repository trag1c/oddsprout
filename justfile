_default:
    @just --list

# runs pytest and strict mypy
test:
    uv run pytest
    uv run mypy --strict src tests

# runs ruff lint and format checks
lint:
    uv run ruff check
    uv run ruff format --check

# checks test and docstring coverage
coverage:
    uv run pytest --cov=src --cov-report term-missing
    uv run interrogate

# runs the ruff formatter and ruff's isort
fmt:
    uv run ruff format
    uv run ruff check --select=I --fix
