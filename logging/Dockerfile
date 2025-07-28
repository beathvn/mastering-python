# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy only files needed for installing dependencies
COPY ./pyproject.toml ./uv.lock ./

# ——————————————————————————————————————————————
# 2. Set env vars for:
#    • in-project venv
#    • HTTP Basic auth for your "devops" registry
# ——————————————————————————————————————————————
ENV UV_PROJECT_ENVIRONMENT=".venv"

# Install uv
RUN pip install --no-cache-dir uv && \
    uv sync --no-dev --frozen --no-install-project && \
    uv cache prune && \
    rm -rf ~/.cache/pip

# Runtime stage
FROM python:3.12-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app/.venv /app/.venv
COPY ./src/ /app/src/

# Set PATH to use the virtualenv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PATH"

# Clean up apt cache and temporary files
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

CMD ["sh", "src/entrypoint.sh"]