# [PROJECT_NAME] Constitution
<!--
SYNC IMPACT REPORT
Version change: N/A (initial version) → 1.0.0
Modified principles: N/A (new principles added)
Added sections: All sections (initial constitution)
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending
  - .specify/templates/spec-template.md ⚠ pending
  - .specify/templates/tasks-template.md ⚠ pending
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->
# In-Memory Todo CLI Application Constitution

## Core Principles

### Object-Oriented Design
Code must follow OOP principles (encapsulation, single responsibility). Modules and classes must have single responsibility and clear separation of concerns.

### Simplicity
Prefer simple data structures and explicit, readable control flow. Code must be readable and understandable by a junior developer. Cyclomatic complexity should remain low.

### Determinism
Same inputs must always produce the same outputs during a single runtime. Tasks must have stable, deterministic IDs for the lifetime of the process.

### Engineering Standards
Language: Python 3.13+. Runtime: uv. Interface: Command-line only. Storage: In-memory only. Dependency policy: Use only approved libraries (questionary for CLI interaction).

### Error Handling
Graceful handling of invalid input and non-existent task IDs. No side effects beyond standard input/output.

### Architecture Constraints
Single-responsibility modules. Clear separation of concerns (CLI, domain logic, in-memory storage). No global mutable state outside the designated in-memory task store.

## Feature Scope
Core features: Add Task (title, description), View Task List (including completion status), Update Task (title and/or description), Delete Task (by ID), Mark Task as Complete or Incomplete. Explicit Non-Goals: No persistence across runs, no authentication or multi-user support, no networking, APIs, or external services, no background jobs or scheduling, no AI or ML features.

## Quality Bar
Modules and classes must be intention-revealing. CLI output must be consistent, predictable, and user-friendly. No dead code, unused abstractions, or speculative features.

## Governance
All implementations must follow these principles. Code must be deterministic and clean. All five core features must be implemented exactly as specified.

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
