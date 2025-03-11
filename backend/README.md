# Sheethub Backend

FastAPI-based backend service for Sheethub project.

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv venv
uv pip install -e .
```

## Development

Run the development server:
```bash
uvicorn app.main:app --reload
```

## Testing

Run tests using pytest:
```bash
pytest
```
