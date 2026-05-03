FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set production environment variables
ENV FLASK_ENV=production
ENV EMBEDDING_WARMUP_ON_START=false
ENV EMBEDDING_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

# Create upload folder
RUN mkdir -p backend/uploads

# Expose port
EXPOSE 8080

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--worker-class", "sync", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "backend.run:app"]
