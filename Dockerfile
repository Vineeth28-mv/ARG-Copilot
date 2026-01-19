# Multi-stage build for production-ready container
# Build: docker build -t arg-framework:latest .
# Run: docker run -e OPENAI_API_KEY=xxx -p 8000:8000 arg-framework:latest

# Stage 1: Base image with dependencies
FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy installed packages from base stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY run_example.py .
COPY quick_test.py .

# Create runs directory for outputs
RUN mkdir -p /app/runs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Default command: Run API server
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]

# Alternative commands (override with docker run):
# CLI mode: docker run arg-framework python -m app.cli --query "..."
# Custom script: docker run arg-framework python run_example.py
