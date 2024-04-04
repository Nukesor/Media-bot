default: run

run:
    poetry run python main.py run

setup:
    poetry install

lint:
    poetry run ruff check ./mediabot --output-format=full
    poetry run ruff format ./mediabot --diff

format:
    poetry run ruff check --fix ./mediabot
    poetry run ruff format ./mediabot


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
