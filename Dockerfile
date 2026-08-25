# Use official secure, lightweight runtime architecture
FROM python:3.11-slim

# Establish internal working space inside container
WORKDIR /app

# Install git system dependencies to download remote libraries via pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install cached requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Deploy the service application script
COPY app.py .

# Open internal service port layer
EXPOSE 8000

# Execute service wrapper with production-grade binding
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
