#!/bin/bash

watchexec -w ./ -s SIGINT -r "poetry run python3 ./main.py"
