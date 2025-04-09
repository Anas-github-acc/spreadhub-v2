$ErrorActionPreference = "Stop"

# Set-PSDebug -Trace 1# Turn on debugging
Set-PSDebug -Trace 0 # Turn off debugging

# Activate the virtual environment (Adjust path if needed)
. .\.venv\Scripts\activate

# Run FastAPI in development mode
python -m fastapi dev app/main.py