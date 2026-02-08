# FastAPI Project Folder Structure

Recommended project structure for maintainable FastAPI applications:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application factory and main app
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   └── routes/
│   │   │       ├── __init__.py
│   │   │       ├── users.py
│   │   │       └── items.py
│   ├── models/              # Pydantic models and database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/             # API schemas (request/response)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── database/            # Database configuration
│   │   ├── __init__.py
│   │   ├── base.py          # Base SQLModel classes
│   │   └── session.py       # Async session management
│   ├── repositories/        # Repository pattern implementations
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── user.py
│   ├── dependencies/        # Dependency injection
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   └── helpers.py
│   ├── config/              # Configuration
│   │   ├── __init__.py
│   │   └── settings.py
│   └── exceptions/          # Custom exceptions
│       ├── __init__.py
│       └── handlers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_main.py
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           └── test_users.py
├── requirements.txt
├── requirements-dev.txt
└── .env.example
```

## Key Components Explanation

### App Directory Structure
- `main.py`: Contains the FastAPI app instance and application factory pattern
- `api/`: Contains all API route definitions organized by version
- `models/`: SQLModel database models with table definitions
- `schemas/`: Pydantic schemas for request/response validation
- `repositories/`: Data access layer using repository pattern
- `database/`: Database configuration and session management
- `dependencies/`: FastAPI dependencies for authentication, etc.
- `utils/`: Helper functions and utility classes
- `config/`: Application settings and configuration
- `exceptions/`: Custom exception classes and handlers

### Test Directory Structure
- `conftest.py`: Pytest fixtures and configuration
- Organized by API versions to mirror the app structure
- Separate test files for each route module

### Requirements Files
- `requirements.txt`: Production dependencies
- `requirements-dev.txt`: Development and testing dependencies