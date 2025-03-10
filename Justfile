default: run

run:
    uv run main.py run

setup:
    uv sync

lint:
    uv run ruff check ./mediabot --output-format=full
    uv run ruff format ./mediabot --diff
    taplo format --check

format:
    uv run ruff check --fix ./mediabot
    uv run ruff format ./mediabot
    taplo format


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
