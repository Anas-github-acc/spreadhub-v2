#!/bin/bash
set -e # this will cause the script to exit if any command fails
set -x  # this will cause the script to print each command before running it

# Run tests with coverage for the entire app package
coverage run --source=app -m pytest "./app/tests/test_routes_spreadsheets.py"
coverage report --show-missing 
coverage html --title "Coverage Report: ${@-coverage}" # this will generate a coverage report in the htmlcov directory

