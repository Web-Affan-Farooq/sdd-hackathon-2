# Backend Development Framework

This project provides a standardized backend development framework that gives developers a consistent environment, architecture patterns, and API development guidelines. This enables efficient backend service creation with standardized tools, configurations, and best practices.

## Features

- Standardized development environment setup
- Robust backend service architecture patterns
- Consistent API development guidelines
- Automated testing framework
- Containerization support with Docker
- Database migration capabilities

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Git
- A modern terminal/shell

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/backend-development-framework.git
cd backend-development-framework
```

### 2. Install Dependencies

Using pip:
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements/dev.txt
```

Or using Docker:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

### 3. Environment Configuration

Set up your environment variables by copying the example file:

```bash
cp .env.example .env
# Edit .env with your specific configuration
```

### 4. Initialize Database

```bash
# Run database migrations
cd backend
alembic upgrade head
```

### 5. Run the Application

For development:
```bash
# Activate virtual environment
source venv/bin/activate

# Run the development server
uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000
```

For production:
```bash
# Using Docker
docker-compose -f docker/docker-compose.yml up -d
```

## Architecture Guidelines

This framework implements a service-oriented architecture with the following patterns:

- Models: Define data structures and validation rules
- Services: Contain business logic and orchestrate operations
- API Layer: Exposes functionality through well-defined endpoints
- Configuration: Manages environment-specific settings

## API Development Guidelines

All APIs should follow these consistent patterns:

- Use RESTful conventions where appropriate
- Implement proper error handling with consistent error formats
- Document endpoints using the standardized API contract system
- Follow security best practices (authentication, authorization)

## Running Tests

Unit tests:
```bash
cd backend
pytest tests/unit/
```

Integration tests:
```bash
cd backend
pytest tests/integration/
```

All tests:
```bash
cd backend
pytest
```

## API Documentation

The API documentation is automatically generated with FastAPI and available at:
- Interactive documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc

## Building and Deploying

To build a Docker image:
```bash
docker build -t backend-dev-framework:latest -f docker/Dockerfile .
```

To run the built image:
```bash
docker run -p 8000:8000 backend-dev-framework:latest
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `.env` or terminate the process using the port
2. **Dependency conflicts**: Recreate the virtual environment and reinstall dependencies
3. **Database connection errors**: Verify database configuration in `.env` and ensure database is running

### Health Checks

Run the health check script to verify your environment:
```bash
python backend/scripts/health_check.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request