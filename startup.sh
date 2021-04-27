#!/bin/bash

set -euo pipefail

# Install Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
poetry_exe=$HOME/.poetry/bin/poetry

# Install dependencies
$poetry_exe install --no-dev

# Start application
$poetry_exe run python app/main.py
