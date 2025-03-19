# Stage 1: Build dependencies
FROM python:3.12-alpine AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /bin/uv
RUN chmod +x /bin/uv

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies in one step
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev && \
    find /app/.venv \( -type d -a \( -name test -o -name tests \) \) -o \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) -exec rm -rf '{}' \+

# Copy only necessary app code
COPY scripts ./scripts
COPY app ./app

# Stage 2: Runtime image
FROM python:3.12-alpine

WORKDIR /app

# Copy virtual environment and app code
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/app /app/app
COPY --from=builder /app/scripts /app/scripts

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

CMD ["fastapi", "run", "--workers", "4", "app/main.py", "--port", "8000"]