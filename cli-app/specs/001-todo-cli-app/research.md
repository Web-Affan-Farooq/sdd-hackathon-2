# Research: In-Memory Todo CLI Application

## Decision: Task ID Strategy
**Rationale**: Using auto-incrementing integer IDs starting from 1, stored in-memory only. This ensures deterministic IDs that persist during runtime as required by the constitution. IDs will be assigned sequentially and remain stable even when tasks are deleted (gaps will remain in the sequence).

**Alternatives considered**: 
- UUIDs: Would provide uniqueness but would be less user-friendly for CLI interaction
- Timestamp-based: Would not be deterministic or sequential
- Hash-based: Would be complex and not sequential

## Decision: CLI Framework (Questionary)
**Rationale**: Questionary provides an elegant way to build interactive CLI applications with minimal code. It offers various prompt types (text, select, confirm) that are perfect for a todo application. It aligns with the requirement to use questionary as specified in the constraints.

**Alternatives considered**:
- argparse: More traditional but less interactive
- click: Good but would require more setup for interactive features
- cmd2: More complex than needed for this application

## Decision: Project Structure
**Rationale**: The layered architecture (CLI → Services → Models → Storage) provides clear separation of concerns as required by the constitution. Each layer has a single responsibility and can be tested independently.

**Alternatives considered**:
- Monolithic structure: Would violate single-responsibility principle
- More complex architectures: Would violate simplicity principle

## Decision: In-Memory Storage Implementation
**Rationale**: Using a Python dictionary with integer keys for fast O(1) lookups. The storage will be encapsulated in a class that manages the task collection and ID assignment. This satisfies the in-memory only requirement and provides the deterministic behavior required.

**Alternatives considered**:
- List-based storage: Would make lookups O(n) and complicate ID management
- External storage: Would violate in-memory only constraint
