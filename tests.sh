#!/bin/sh

# Run core tests
python3 -m unittest discover -p "*.py" ./tests/core

# Run docs examples tests
python3 -m unittest discover -p "*.py" ./tests/docs_examples