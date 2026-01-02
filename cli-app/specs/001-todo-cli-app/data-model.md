# Data Model: In-Memory Todo CLI Application

## Task Entity

### Fields
- **id**: Integer - Unique identifier assigned sequentially, remains stable during runtime
- **title**: String - Required task title provided by user
- **description**: String - Optional task description provided by user  
- **completed**: Boolean - Task completion status (default: False)

### Relationships
- None (standalone entity)

### Validation Rules
- Title must not be empty or only whitespace
- ID must be positive integer
- Completed status must be boolean

### State Transitions
- **Incomplete → Complete**: When user marks task as complete
- **Complete → Incomplete**: When user marks task as incomplete

## In-Memory Store

### Structure
- **tasks**: Dictionary mapping integer IDs to Task objects
- **next_id**: Integer counter for assigning next available ID

### Operations
- **Create**: Add new task with auto-assigned ID
- **Read**: Retrieve task by ID
- **Update**: Modify existing task properties
- **Delete**: Remove task by ID
- **List**: Return all tasks
