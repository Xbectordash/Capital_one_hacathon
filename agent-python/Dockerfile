
# Use official Python image as a parent image
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
    && rm -rf /var/lib/apt/lists/*


# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt ./


# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Copy the rest of the application code
COPY . .


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Expose port if needed (adjust as necessary)
EXPOSE 8000


# Run the application
CMD ["python", "main.py"]
