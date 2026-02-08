# Project: Evolution of Todo — Phase II (Full-Stack Web App)

## Overview
Build a multi‑user todo web app with Next.js frontend, FastAPI backend, Neon PostgreSQL, and Better Auth JWT authentication.

## Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind
- **Backend**: FastAPI, SQLModel, Python 3.13+
- **Database**: Neon PostgreSQL (serverless)
- **Auth**: Better Auth (JWT tokens)
- **Spec‑Driven**: Claude Code + Spec‑Kit Plus

## Development Rules
1. **Monorepo layout**: `/frontend`, `/backend`, `/specs`
2. **Always spec‑first**: Write specs in `/specs` before any implementation.
3. **No manual coding**: Use Claude Code to generate code from specs.
4. **JWT authentication**: All API calls require `Authorization: Bearer <token>`.
5. **User isolation**: Backend must filter all data by `user_id` from JWT.

## Key Directories
- `/specs/features` – User stories & acceptance criteria
- `/specs/api` – REST endpoint specifications
- `/specs/database` – Schema definitions
- `/frontend` – Next.js app
- `/backend` – FastAPI app

## Workflow
1. Update or create spec in `/specs`.
2. Reference spec in prompt: `@specs/features/task-crud.md`
3. Let Claude Code generate implementation.
4. Test and refine spec if output is incorrect.

## Phase II Goals
- Implement Basic, Intermediate & Advanced todo features (see specs).
- Deploy frontend on Vercel, backend on a public URL.
- Submit: GitHub repo, live URLs, 90‑second demo video.

## Notes
- Windows users: Develop under WSL 2.
- All environment variables (e.g., `DATABASE_URL`, `BETTER_AUTH_SECRET`) must be set.
- Follow clean code and consistent project structure.