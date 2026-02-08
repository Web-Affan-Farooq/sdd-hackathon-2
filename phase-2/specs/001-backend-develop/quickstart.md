# Quickstart Guide: Backend Development Framework

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
pip install -r requirements/dev.txt
```

Or using Docker:
```bash
docker-compose up --build
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
python -m alembic upgrade head
```

### 5. Run the Application

For development:
```bash
# Activate virtual environment
source venv/bin/activate

# Run the development server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

For production:
```bash
# Using Docker
docker-compose -f docker/docker-compose.yml up -d
```

## Creating a New Service

1. Create a new service module in `src/services/`
2. Define your models in `src/models/`
3. Create API endpoints in `src/api/v1/`
4. Write unit tests in `tests/unit/`
5. Write integration tests in `tests/integration/`

Example service structure:
```
src/
├── services/
│   └── my_new_service.py
├── models/
│   └── my_model.py
└── api/
    └── v1/
        └── my_endpoint.py
```

## Running Tests

Unit tests:
```bash
pytest tests/unit/
```

Integration tests:
```bash
pytest tests/integration/
```

All tests:
```bash
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
python scripts/health_check.py
```

## Next Steps

1. Explore the API documentation at `/docs`
2. Review the example services in `src/services/`
3. Customize the environment configuration in `.env`
4. Add your own services following the established patterns