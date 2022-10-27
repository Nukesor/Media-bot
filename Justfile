default: run

run:
    poetry run python main.py run

setup:
    poetry install

lint:
    poetry run black --check mediabot
    poetry run isort --check-only mediabot
    poetry run flake8 mediabot

format:
    # remove unused imports
    poetry run autoflake \
        --remove-all-unused-imports \
        --recursive \
        --in-place mediabot
    poetry run black mediabot
    poetry run isort mediabot


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
