# Backend Guidelines – Phase II

## Stack
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL (serverless)
- **Auth**: JWT (via Better Auth)
- **Python**: 3.13+ (UV environment)

## Project Structure
```
/backend
├── main.py              # FastAPI app entry point
├── models.py            # SQLModel database models
├── schemas.py           # Pydantic request/response models
├── database.py          # DB connection & session
├── dependencies.py      # Auth dependencies (JWT verification)
├── routes/
│   ├── tasks.py         # Task CRUD endpoints
│   └── auth.py          # Auth‑related endpoints (if needed)
└── .env                 # Environment variables
```

## Authentication
- All endpoints require JWT in header: `Authorization: Bearer <token>`
- Token secret: `BETTER_AUTH_SECRET` (same as frontend)
- Extract `user_id` from token; match with URL `user_id` for isolation
- Unauthorized requests → `401`
- Use `dependencies.py` for reusable auth logic

## API Endpoints (all under `/api/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List tasks (supports filter, sort, search) |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get single task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## Database Models (SQLModel)
- **User** (managed by Better Auth): `id`, `email`, `name`, `created_at`
- **Task**:  
  `id`, `user_id` (FK), `title`, `description`, `completed` (bool),  
  `priority` (high/medium/low), `tags` (JSON array), `due_date` (datetime),  
  `is_recurring` (bool), `recurrence_rule` (text), `created_at`, `updated_at`

## Feature Implementation Notes
1. **Basic CRUD**: Validate title (1‑200 chars), description optional.
2. **Priorities & Tags**: Store as strings/enums; tags as JSON array.
3. **Search & Filter**:  
   - Search: ILIKE on title/description  
   - Filter: by `completed`, `priority`, `due_date` ranges  
   - Sort: by `due_date`, `priority`, `title`, `created_at`
4. **Recurring Tasks**:  
   - Use `recurrence_rule` (e.g., `"FREQ=WEEKLY"`)  
   - Auto‑reschedule when marked complete (background job/cron)
5. **Due Dates & Reminders**:  
   - Store `due_date` (datetime)  
   - Reminder logic: publish event to Kafka (Phase V) or schedule job

## Code Conventions
- Use Pydantic models for request/response validation.
- Raise `HTTPException` with appropriate status codes.
- All database operations via SQLModel sessions.
- Environment variables: `DATABASE_URL`, `BETTER_AUTH_SECRET`.


## Spec‑Driven Development
- Backend specs are in `/specs/api/` and `/specs/database/`
- Always reference spec files: `@specs/api/rest-endpoints.md`
- Let Claude Code generate the implementation; refine spec if needed.

## Security
- Never expose user data across accounts.
- Validate `user_id` from JWT matches resource ownership.
- Use parameterized queries (SQLModel does this).
- Keep secrets in environment, not in code.

## Next Steps
- After backend, integrate with frontend (Next.js).
- Deploy backend publicly (e.g., Railway, Fly.io) for Phase II submission.
