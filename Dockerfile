# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies
# --frozen: strict version matching using lockfile
# --no-dev: do not install dev dependencies
RUN uv sync --frozen --no-dev --no-install-project

# Copy source code
COPY . .

# Expose the server port
EXPOSE 2222

# Run the server
# Use `uv run` to ensure we run within the virtual environment
CMD ["uv", "run", "python", "-m", "src.server"]
