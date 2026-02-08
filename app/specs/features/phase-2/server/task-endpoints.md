# Task REST API Endpoints Specification

## Endpoint Patterns

**Base Structure:**
- All endpoints under `/api/{user_id}/` prefix
- `user_id` extracted from JWT token for ownership verification
- RESTful HTTP methods (GET, POST, PUT, DELETE, PATCH)

**CRUD Operations:**
- `GET /tasks`: List tasks with filters (status, priority, search)
- `POST /tasks`: Create new task with validation (title: 1-200 chars)
- `GET /tasks/{id}`: Retrieve single task by ID
- `PUT /tasks/{id}`: Full task update
- `DELETE /tasks/{id}`: Remove task permanently
- `PATCH /tasks/{id}/complete`: Toggle completion status

**Filtering & Sorting:**
- Query parameters: `status`, `priority`, `due_date_range`
- Search: Case-insensitive text search on title/description
- Sort options: due_date, priority, title, created_at

**Data Validation:**
- Required fields enforced server-side
- Priority: enum (high/medium/low)
- Tags: JSON array storage
- Recurrence rules: RFC 5545 format support