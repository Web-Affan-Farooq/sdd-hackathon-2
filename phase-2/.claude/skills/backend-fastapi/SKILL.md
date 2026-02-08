---

name: backend-fastapi
description: |
  This skill should be used when building complete end-to-end backends with the FastAPI framework, testing FastAPI applications, or refactoring existing FastAPI projects.
  It provides comprehensive guidance for developing production-ready FastAPI applications with proper architecture, testing, and code organization.
  NOTE: This skill handles backend API development, database integration, and core service logic. It does NOT handle containerization (use production-dockerfile skill),
  advanced AI/ML integrations (use appropriate AI skills), or frontend development (use react-development, frontend-design, or building-with-nextjs skills).
---

# FastAPI Backend Development Skill

This skill provides comprehensive guidance for developing complete end-to-end backends with the FastAPI framework, testing applications effectively, and refactoring existing FastAPI projects.

## Skill Boundaries and Complementary Skills

This skill focuses specifically on:
- FastAPI backend development and API design
- SQLModel and PostgreSQL integration
- Async database operations
- API authentication and security
- Service architecture and patterns

For complementary functionality, delegate to these specialized skills:
- **Containerization**: Use `production-dockerfile` skill for Docker configuration
- **Frontend Integration**: Use `building-with-nextjs`, `react-development`, or `frontend-design` skills
- **AI/ML Features**: Use appropriate AI/ML-focused skills
- **Testing**: While this skill includes testing patterns, specialized testing skills can enhance coverage
- **Deployment**: Use deployment-specific skills for platform-specific configurations

## What This Skill Does

- Develop complete end-to-end backends with FastAPI framework which seamlessly integrates with any framework (e.g., Next.js, etc.)
- Create well-structured, maintainable FastAPI applications following [best practices](./references/best-practices.md)
- Implement effective testing strategies for FastAPI applications [See reference](./references/testing-patterns.md)
- Apply refactoring strategies [See reference](./references/refactoring-patterns.md)
- Follow FastAPI best practices and security patterns
- Generate proper documentation and API specifications
- Manage database operations using SQLModel with PostgreSQL [See reference](./references/crud-operations.md)
- Handle async database sessions properly [See reference](./references/database-session.md)

## What This Skill Does NOT Do

- Complete integration of LLMs or AI models
- Model fine-tuning or machine learning implementation
- Deployment configuration or cloud infrastructure (refer to [deployment reference](./references/deployment.md) for guidance)
- AI-specific integrations or machine learning tactics
- Frontend development or UI components

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing FastAPI structure, patterns, dependencies, and conventions to integrate with |
| **Codebase** | Use `fetch-library-docs` skills for getting up-to-date knowledge about FastAPI through [fastapi docs](https://fastapi.tiangolo.com/learn/) |
| **Conversation** | User's specific backend requirements, endpoints, data models, and business logic |
| **Skill References** | FastAPI patterns from `./references/`
| **User Guidelines** | Project-specific conventions, team standards, and architectural preferences |

Ensure all required context is gathered from user as well as from references before implementing.

## Project Structure

Follow the recommended [folder structure](./references/folder-structure.md) for maintainable FastAPI applications.

## Package Management

This skill uses `uv` as the preferred package manager for faster dependency resolution and installation [See reference](./references/dependency-management.md).

## Core Implementation Patterns

Refer to [best practices](./references/best-practices.md) for implementation patterns including:
- Application factory pattern
- Dependency injection and security
- Pydantic models and schemas
- Async session management [See reference](./references/database-session.md)
- Repository patterns [See reference](./references/crud-operations.md)

## Testing Strategies

Implement testing using patterns outlined in [testing reference](./references/testing-patterns.md), including:
- Async testing with Pytest
- Database testing with test sessions
- API endpoint testing
- Security and authentication testing

## Refactoring Guidelines

When refactoring existing FastAPI projects, follow guidelines in [refactoring reference](./references/refactoring-patterns.md).

## Security and Performance

Apply security considerations and performance optimizations as detailed in [best practices reference](./references/best-practices.md).

## Deployment

For deployment options and configurations, see [deployment reference](./references/deployment.md).

## MCP Server Integration

For detailed FastAPI documentation, database schemas, and up-to-date patterns, use the `context7` MCP server instead of relying on static references [See reference](./references/context-server-integration.md). The server can provide:
- Latest FastAPI documentation and API references
- Updated SQLModel/SQLAlchemy patterns
- Current security best practices
- Database optimization techniques
- Performance tuning recommendations

## Testing Checklist

Use the comprehensive [testing checklist](./references/testing-patterns.md#testing-checklist) to ensure complete test coverage.