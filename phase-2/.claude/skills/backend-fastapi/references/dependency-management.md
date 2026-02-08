# Dependency Management with UV

This reference covers dependency management using the `uv` package manager for FastAPI projects.

## Installing UV Package Manager

```bash
# Install uv globally
pip install uv

# Or install using the official installer
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## UV Commands for FastAPI Projects

### Installing Dependencies

```bash
# Install from requirements.txt
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt

# Install a specific package
uv pip install fastapi

# Install with extras
uv pip install fastapi[all]
```

### Managing Virtual Environments

```bash
# Create a new virtual environment
uv venv

# Activate the virtual environment (Unix/Mac)
source .venv/bin/activate

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Install packages in the virtual environment
uv pip install -r requirements.txt
```

## Recommended Requirements Files

### requirements.txt
```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
sqlmodel>=0.0.16
sqlalchemy>=2.0.23
asyncpg>=0.29.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
alembic>=1.13.1
httpx>=0.25.2
python-multipart>=0.0.6
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0
```

### requirements-dev.txt
```
-r requirements.txt
pytest>=7.4.3
pytest-asyncio>=0.21.1
pytest-cov>=4.1.0
black>=23.11.0
isort>=5.12.0
flake8>=6.1.0
mypy>=1.7.1
pre-commit>=3.5.0
faker>=22.0.0
```

## UV Advantages for FastAPI Development

- **Faster Installation**: UV is significantly faster than pip for installing packages
- **Better Dependency Resolution**: More efficient dependency resolution algorithm
- **Lock File Generation**: Generate lock files for reproducible builds
- **Virtual Environment Management**: Built-in virtual environment tools

## Best Practices

- Use `uv` for all dependency management in FastAPI projects
- Maintain separate requirements files for production and development
- Pin major and minor versions in production requirements
- Use virtual environments for isolated development
- Regularly update dependencies using `uv pip sync`