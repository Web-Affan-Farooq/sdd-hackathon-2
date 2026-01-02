# Quickstart: In-Memory Todo CLI Application

## Setup

1. Ensure Python 3.13+ is installed
2. Install uv package manager
3. Clone the repository
4. Navigate to the project directory

```bash
# Initialize the project with uv
uv init

# Install dependencies
uv add questionary

# Run the application
uv run src/cli/main.py
```

## Usage

### Add a Task
```bash
python src/cli/main.py add "Task title" "Task description"
```

### List All Tasks
```bash
python src/cli/main.py list
```

### Update a Task
```bash
python src/cli/main.py update 1 "New title" "New description"
```

### Delete a Task
```bash
python src/cli/main.py delete 1
```

### Mark Task as Complete
```bash
python src/cli/main.py complete 1
```

### Mark Task as Incomplete
```bash
python src/cli/main.py incomplete 1
```

## Development

1. Set up virtual environment with uv
2. Install dependencies: `uv add questionary`
3. Run tests: `uv run pytest`
4. Run the application: `uv run src/cli/main.py [command]`
