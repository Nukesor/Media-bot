#!/bin/bash

watchexec -w ./ -s SIGINT -r "poetry run python3 ./telethon_bot.py"
