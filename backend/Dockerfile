FROM python:3.13-alpine

# setting workking directory
WORKDIR /app/

# ------------------------------------------------------------------------------
# Install uv from the official image
# Ref: https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
# ------------------------------------------------------------------------------
COPY --from=ghcr.io/astral-sh/uv:0.5.30 /uv /bin/uv

# setting the environment variable
ENV PATH="/app/.venv/bin:$PATH" \
UV_COMPILE_BYTECODE=1 \
UV_LINK_MODE=copy

# ------------------------------------------------------------------------------
# Pre-install dependencies (without installing the project) using uv.
# This leverages Docker cache so that changes in the project code don't force re-installation of dependencies.
# ------------------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock,readonly \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml,readonly \
    uv sync --frozen --no-install-project

# ------------------------------------------------------------------------------
# Set PYTHONPATH so that the application code is discoverable.
# ------------------------------------------------------------------------------
ENV PYTHONPATH=/app

# ------------------------------------------------------------------------------
# Copy application-specific files:
# - Scripts (if any)
# - Dependency configuration files (pyproject.toml, uv.lock, alembic.ini)
# - Application source code
# ------------------------------------------------------------------------------
COPY ./scripts /app/scripts
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
COPY ./app /app/app

# ------------------------------------------------------------------------------
# Final synchronization: install project dependencises and compile the project.
# this will pick up any changes in your source code or dependency configuration.
# ------------------------------------------------------------------------------
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# EXpose the port
EXPOSE 8000


# command to run the application
CMD ["fastapi", "dev", "app/main.py"]


