$ErrorActionPreference = "Stop"

# Display commands being run
Set-PSDebug -Trace 1

# Activate the virtual environment (Adjust path if needed)
. .\.venv\Scripts\activate

# Run FastAPI in development mode
fastapi dev app/main.py