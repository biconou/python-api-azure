#!/bin/bash

# Install Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry_exe=$HOME/.poetry/bin/poetry

# Install dependencies
$poetry_exe install

# Start application
$poetry_exe run python app/main.py
