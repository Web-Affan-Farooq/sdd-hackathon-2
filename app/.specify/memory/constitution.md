<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: None (new constitution)
Added sections: All sections based on Phase II requirements
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md - Updated to reflect new principles
- ✅ .specify/templates/spec-template.md - Updated to reflect new requirements
- ✅ .specify/templates/tasks-template.md - Updated to reflect new task types
- ⚠️ .specify/templates/commands/*.md - May need review for outdated references
- ⚠️ README.md - May need review for updated principles
Follow-up TODOs: None
-->
# Phase II — Full-Stack Todo Web Application Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All development must follow the Specify → Plan → Tasks → Implement workflow. No manual coding is allowed; all code must be generated via Claude Code from approved specs. This ensures deterministic behavior over creative implementation and maintains traceability between specifications and generated code.

### II. Security-First Architecture
User isolation and security are non-negotiable requirements. Every API request must require a valid JWT for authentication. User identity must be derived from JWT, never from client input. All queries must be scoped by authenticated user_id. Secrets must come from environment variables; never hardcoded. Tasks must always belong to exactly one user with no cross-user reads or writes under any circumstance.

### III. Backend as Single Source of Truth
The backend serves as the authoritative data layer with the frontend acting as a pure consumer. This separation ensures data integrity and centralized business logic. All database operations must go through properly authenticated API endpoints, enforcing REST architecture without server actions bypassing the API.

### IV. Deterministic Behavior Over Creative Implementation
Implementation must follow precise specifications rather than creative interpretation. No AI features, chat interfaces, MCP tools, or background workers are allowed in the core application. This ensures predictable, testable, and maintainable code that meets exact requirements.

### V. Monorepo with Spec-Kit Structure
Maintain a unified codebase with Spec-Kit organization where specs serve as the authoritative source for all development. This enables coordinated evolution of frontend, backend, and specification artifacts while maintaining clear architectural boundaries between components.

### VI. End-to-End JWT Authentication Enforcement
Authentication must be implemented consistently across the entire stack using Better Auth for frontend and JWT verification for backend. This creates a unified security model where user context flows seamlessly from the UI through the API to the database layer.

## Technical Architecture Constraints

### Frontend Requirements
- Technology Stack: Next.js (App Router) with TypeScript
- Architecture: Pure consumer of backend APIs
- Authentication: Better Auth integration for user management
- Structure: Follow App Router conventions with proper component organization

### Backend Requirements
- Technology Stack: FastAPI (Python) with SQLModel ORM
- Database: Neon Serverless PostgreSQL only
- Architecture: REST API with proper error handling and HTTP status codes
- Authentication: JWT verification for all protected endpoints

### Data Integrity and Migration Rules
- Database Schema: Changes require spec updates before implementation
- User Isolation: Strict enforcement of user boundaries in all queries
- Migration Strategy: Proper migration and rollback procedures for schema changes
- Data Retention: Follow established policies for data lifecycle management

## Development Workflow and Quality Standards

### Specification Requirements
- All endpoints must be documented in specs before implementation
- Error handling must be explicit and consistent across all APIs
- Acceptance criteria must be clearly defined and testable
- Cross-cutting concerns (auth, validation, error handling) must be specified

### Implementation Standards
- Code Generation: Use Claude Code exclusively from approved specs
- Testing: All functionality must have appropriate test coverage
- Code Quality: Follow established patterns and maintain consistency
- Documentation: Maintain up-to-date API documentation and developer guides

## Governance

This constitution establishes the fundamental rules governing all development activities for the Phase II Full-Stack Todo Web Application. All team members must adhere to these principles, and any deviations require explicit constitutional amendments. The constitution supersedes all other development practices and serves as the ultimate authority for architectural decisions.

All pull requests and code reviews must verify compliance with constitutional principles. Any implementation that violates these core principles must be rejected until alignment is achieved. The constitution ensures that Phase III and subsequent phases can be built upon these stable, secure, and well-defined foundations without requiring refactoring of Phase II components.

**Version**: 1.0.0 | **Ratified**: 2026-02-07 | **Last Amended**: 2026-02-07