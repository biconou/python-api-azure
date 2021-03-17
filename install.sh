#!/bin/bash

echo "Install Poetry"
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
export poetry_exe=$HOME/.poetry/bin/poetry

echo "Install dependencies"
$poetry_exe install

