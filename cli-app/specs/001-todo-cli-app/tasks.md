---
description: "Task list template for feature implementation"
---

# Tasks: In-Memory Todo CLI Application

**Input**: Design documents from `/specs/001-todo-cli-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

<!--
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.

  The /sp.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/

  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment

  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with src/, tests/ directories
- [X] T002 Initialize Python project with uv and create pyproject.toml
- [X] T003 [P] Install questionary dependency using uv

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [X] T004 Create base Task model in src/models/task.py with id, title, description, completed fields
- [X] T005 [P] Create in-memory storage class in src/storage/in_memory_store.py with auto-incrementing IDs
- [X] T006 [P] Create todo service in src/services/todo_service.py with basic CRUD operations
- [X] T007 Create CLI argument parser in src/cli/main.py with add, list, update, delete, complete, incomplete commands
- [X] T008 Configure error handling for invalid input and missing task IDs

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with titles and descriptions and view them in a list

**Independent Test**: Can be fully tested by adding a task and viewing the task list. Delivers the basic value of a todo application.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Unit test for Task model in tests/unit/test_task.py
- [X] T011 [P] [US1] Integration test for add/list operations in tests/integration/test_todo_service.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement Task model with validation in src/models/task.py
- [X] T013 [US1] Implement add_task method in src/services/todo_service.py
- [X] T014 [US1] Implement list_tasks method in src/services/todo_service.py
- [X] T015 [US1] Implement add command in src/cli/main.py
- [X] T016 [US1] Implement list command in src/cli/main.py
- [X] T017 [US1] Add CLI output formatting for task list

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Enable users to update existing tasks and delete them

**Independent Test**: Can be fully tested by updating and deleting tasks. Delivers the ability to maintain the todo list over time.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T018 [P] [US2] Integration test for update/delete operations in tests/integration/test_todo_service.py

### Implementation for User Story 2

- [X] T019 [US2] Implement update_task method in src/services/todo_service.py
- [X] T020 [US2] Implement delete_task method in src/services/todo_service.py
- [X] T021 [US2] Implement update command in src/cli/main.py
- [X] T022 [US2] Implement delete command in src/cli/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task Completion Status (Priority: P3)

**Goal**: Enable users to mark tasks as complete or incomplete

**Independent Test**: Can be fully tested by marking tasks as complete/incomplete. Delivers the ability to track task status.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US3] Integration test for complete/incomplete operations in tests/integration/test_todo_service.py

### Implementation for User Story 3

- [X] T024 [US3] Implement mark_complete method in src/services/todo_service.py
- [X] T025 [US3] Implement mark_incomplete method in src/services/todo_service.py
- [X] T026 [US3] Implement complete command in src/cli/main.py
- [X] T027 [US3] Implement incomplete command in src/cli/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T028 [P] Add error handling for non-existent task IDs in all operations
- [X] T029 [P] Add validation for empty titles in all operations
- [X] T030 [P] Improve CLI output formatting and user experience
- [X] T031 [P] Add documentation in README.md
- [ ] T032 Run quickstart validation to ensure all commands work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model in tests/unit/test_task.py"
Task: "Integration test for add/list operations in tests/integration/test_todo_service.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation in src/models/task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence