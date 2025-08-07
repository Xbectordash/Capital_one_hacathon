# Use official Python image as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app


# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose default ChromaDB port (if running as a server, adjust as needed)
EXPOSE 8000

# Set environment variables (optional, adjust as needed)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default command to run starter.py
CMD ["python", "starter.py"]
