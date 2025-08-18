
# FarmMate AI Server - Python FastAPI + WebSocket
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for scientific and cryptography packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements.txt first to leverage Docker cache
COPY requirement.txt ./

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --disable-pip-version-check -r requirement.txt && \
    pip cache purge

# Copy the rest of the application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1001 farmmate-ai && \
    chown -R farmmate-ai:farmmate-ai /app
USER farmmate-ai

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PORT=8000

# Expose port 8000 for FastAPI server
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI server
CMD ["python", "src/start_server.py"]
