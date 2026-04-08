# ==============================================================================
# NRC φ^∞ Lattice Compression Engine - Containerization
# ==============================================================================

FROM python:3.12-slim as builder

# Install system dependencies including Rust for compiling the FFI layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Rust (required for building the internal crate)
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install uv – The ultra-fast Python package installer
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency specifications first to leverage Docker cache
COPY pyproject.toml README.md Cargo.toml ./

# Install dependencies using uv into a virtual environment
RUN uv venv .venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Install pure python dependencies and specify pytorch CPU index
RUN uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    && uv pip install mpmath numpy matplotlib jupyter ipykernel ruff mypy pytest hypothesis

# Copy the actual source code
COPY phi_infinity_lattice_compression/ phi_infinity_lattice_compression/
COPY src/ src/

# Build and install the package itself (including Rust bindings)
RUN uv pip install -e .

# ------------------------------------------------------------------------------
# Production Image
# ------------------------------------------------------------------------------
FROM python:3.12-slim

WORKDIR /app

# Copy the virtual environment and source from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Setup non-root user for security (TTT safety constraint)
RUN useradd -m nrc_user
RUN chown -R nrc_user:nrc_user /app
USER nrc_user

# Default command: expose a Jupyter Lab testing environment on port 8888 
# or run the unified CLI. Default to generic bash unless overridden.
CMD ["python", "-c", "import phi_infinity_lattice_compression; print('φ^∞ Lattice Compression Container Online.')"]
