# Multi-stage build for minimal attack surface
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage - minimal runtime
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application files
COPY --chown=appuser:appuser *.py ./
COPY --chown=appuser:appuser requirements.txt ./

# Create output directory with proper permissions
RUN mkdir -p /app/output && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Default command
CMD ["python", "create-testdata.py", "--help"]