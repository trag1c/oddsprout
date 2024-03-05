_default:
    @just --list    

# runs pytest and strict mypy
test:
    pytest
    mypy --strict oddsprout tests

# runs ruff lint and format checks
lint:
    ruff check
    ruff format --check

# checks test and docstring coverage
coverage:
    coverage run -m pytest
    coverage report -m
    interrogate

# runs the ruff formatter and ruff's isort
format:
    ruff format
    ruff check --select=I --fix
