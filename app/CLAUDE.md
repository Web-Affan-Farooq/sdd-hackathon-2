# Todo App - Hackathon II

## Project Overview
This is a monorepo using GitHub Spec-Kit for spec-driven development.

## Spec-Kit Structure
Specifications are organized in `/specs` directory:
- `/specs/overview.md` - Project overview
- `/specs/features` - Feature specs divided as phases 

## How to Use Specs
1. Always read relevant spec before implementing
2. Reference specs with: `@specs/features/phase[]/example`
3. Update specs if requirements change

## Project Structure
- /frontend - Next.js 14 app
- /backend - Python FastAPI server

## Development Workflow
1. Read spec: @specs/features/phase[phase]/feature
2. Implement backend: @backend/CLAUDE.md
3. Implement frontend: @frontend/CLAUDE.md
4. Test and iterate