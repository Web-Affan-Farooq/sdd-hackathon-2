# In-Memory Todo CLI Application

A clean, deterministic, in-memory Todo application for the command line built with Python and questionary.

## Features

- Add tasks with titles and descriptions
- View all tasks with completion status
- Update existing tasks
- Delete tasks
- Mark tasks as complete or incomplete
- In-memory storage (no persistence across runs)
- Interactive CLI with questionary prompts

## Requirements

- Python 3.13+
- uv package manager

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies using uv:

```bash
uv sync
```

## Usage

### Add a Task
```bash
uv run src/cli/main.py add "Task title" "Task description"
```

### List All Tasks
```bash
uv run src/cli/main.py list
```

### Update a Task
```bash
uv run src/cli/main.py update 1 "New title" "New description"
```

### Delete a Task
```bash
uv run src/cli/main.py delete 1
```

### Mark Task as Complete
```bash
uv run src/cli/main.py complete 1
```

### Mark Task as Incomplete
```bash
uv run src/cli/main.py incomplete 1
```

### Interactive Mode
If you don't provide arguments, the application will prompt you interactively:

```bash
uv run src/cli/main.py add
```

## Architecture

The application follows a clean architecture with clear separation of concerns:

- **Models**: Task entity with validation
- **Storage**: In-memory storage with auto-incrementing IDs
- **Services**: Business logic layer
- **CLI**: Command-line interface with argument parsing and interactive prompts

## Development

1. Set up the development environment:
   ```bash
   uv sync
   ```

2. Run the application:
   ```bash
   uv run src/cli/main.py [command]
   ```

3. Run tests:
   ```bash
   uv run pytest
   ```

## Design Principles

- **Object-Oriented Design**: Code follows OOP principles with encapsulation and single responsibility
- **Simplicity**: Uses simple data structures and readable control flow
- **Determinism**: Same inputs produce same outputs during runtime; stable task IDs
- **Error Handling**: Graceful handling of invalid input and non-existent task IDs

## Project Structure

```
src/
├── models/
│   └── task.py          # Task entity
├── services/
│   └── todo_service.py  # Business logic
├── storage/
│   └── in_memory_store.py  # In-memory storage
└── cli/
    └── main.py          # CLI interface
tests/
├── unit/
│   └── test_task.py     # Unit tests
└── integration/
    └── test_todo_service.py  # Integration tests
```