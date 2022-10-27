default: run

run:
    poetry run python main.py run

setup:
    poetry install

lint:
    poetry run black --check mediabot
    poetry run isort \
        --skip __init__.py \
    --check-only mediabot
    poetry run flake8 \
        --per-file-ignore=mediabot/telethon/media.py:W605 \
        mediabot

format:
    # remove unused imports
    poetry run autoflake \
        --remove-all-unused-imports \
        --recursive \
        --exclude=__init__.py,.venv \
        --in-place mediabot
    poetry run black mediabot
    poetry run isort mediabot \
        --skip __init__.py


# Watch for something
# E.g. `just watch lint` or `just watch test`
watch *args:
    watchexec --clear 'just {{ args }}'
