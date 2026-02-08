# FastAPI Deployment Patterns

This reference covers deployment strategies for FastAPI applications.

## Hugging Face Spaces Deployment

### Entry Point File
```python
# app.py (entry point for Hugging Face Spaces)
from app.main import app

# Hugging Face Spaces expects a variable called "app"
# The skill already creates this in main.py
```

### Space Configuration
```yaml
# space.yaml
title: FastAPI Backend
emoji: 🚀
color: purple
sdk: docker
runtime:
  cpu: true
  memory: 16GiB
  accelerator: null
```

### Dockerfile for Hugging Face Spaces
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --upgrade pip && pip install uv

# Copy requirements first to leverage Docker cache
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies using uv
RUN uv pip install --system --compile-bytecode -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 7860

# Run the application - Hugging Face uses port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

## Standard Docker Deployment

### Production Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --upgrade pip && pip install uv

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies using uv
RUN uv pip install --system --compile-bytecode -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose for Local Development
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:password@db:5432/myapp
      - SECRET_KEY=your-secret-key-here
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Cloud Platform Deployments

### AWS Elastic Beanstalk
- Use the Dockerfile approach with EB CLI
- Configure environment variables through EB console
- Set up health check endpoints

### Google Cloud Run
- Containerize with Dockerfile
- Deploy using gcloud CLI
- Configure environment variables and scaling options

### Azure Container Instances
- Build and push to Azure Container Registry
- Deploy container with ACI
- Configure networking and security

## Production Considerations

### Environment Variables
- Use environment variables for configuration
- Never hardcode sensitive information
- Use .env.example as template for required variables

### Health Checks
- Implement health check endpoints
- Monitor application and database connectivity
- Set up alerts for unhealthy deployments

### Logging
- Configure structured logging
- Set up log aggregation
- Implement proper log levels

### Monitoring
- Add metrics endpoints
- Monitor response times and error rates
- Track database performance

### Scaling
- Configure horizontal pod autoscaling
- Set up load balancing
- Optimize resource allocation