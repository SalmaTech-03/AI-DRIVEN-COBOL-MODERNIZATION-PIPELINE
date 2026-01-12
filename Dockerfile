FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for Spark/TensorFlow
RUN apt-get update && apt-get install -y default-jdk-headless && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI port
EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]