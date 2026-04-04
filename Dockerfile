# HF Spaces optimized Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_hf.txt .
RUN pip install --no-cache-dir -r requirements_hf.txt

# Copy application files
COPY . .

# Set environment variables for HF Spaces
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    API_BASE_URL="http://localhost:8000" \
    MODEL_NAME="gpt-3.5-turbo"

# Expose port for HF Spaces
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/reset || exit 1

# Run the application on HF Spaces port
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
