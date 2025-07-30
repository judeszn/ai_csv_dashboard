# syntax=docker/dockerfile:1

# ---- Builder Stage ----
FROM python:3.10 AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && pip install --timeout=100 -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.10-slim
WORKDIR /app
ENV GEMINI_MODEL="gemini-2.0-flash"

COPY --from=builder /opt/venv /opt/venv

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Copy application files from the build context
COPY . .

# Set environment variables for the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app

EXPOSE 8000 8501

# Create a non-root user, set permissions, and make the start script executable.
# Also create any directories the app needs to write to at runtime.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser && \
    chown -R appuser:appgroup /app /opt/venv && \
    sed -i 's/\r$//' /app/start.sh && \
    chmod +x /app/start.sh

# Switch to the non-root user for added security
USER appuser

CMD ["./start.sh"]