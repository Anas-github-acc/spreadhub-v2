# Sheethub Backend

FastAPI-based backend service for Sheethub project.

## Manually Setup & Run the Server

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
uv sync
```

## Development

Run the development server:

```bash
fastapi dev app/main.py
# or run this instead
./dev
```

## Testing

Run tests using pytest:

```bash
pytest
```
