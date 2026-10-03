# ==========================================
# STAGE 1: Build & Dependency Resolution
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install basic OS utilities needed for wheel compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create an isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2: Final Minimal Runtime Image
# ==========================================
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime utilities (curl is needed for the Docker healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the pre-compiled virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create a non-root system user for secure container execution
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app/.cache/huggingface && \
    chown -R appuser:appuser /app

# Set Hugging Face cache directory inside the container
ENV HF_HOME="/app/.cache/huggingface"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy application source code
COPY --chown=appuser:appuser app/ /app/app

# Switch to non-root user
USER appuser

# Expose FastAPI default port
EXPOSE 8000

# Docker Healthcheck: Checks if the models are loaded and ready
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/ready || exit 1

# Start the application server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]