set -e # this will cause the script to exit if any command fails
set -x  # this will cause the script to print each command before running it


coverage run --source=app -m pytest
coverage report --show-missing 
coverage html --title "Coverage Report: ${@-coverage}" # this will generate a coverage report in the htmlcov directory