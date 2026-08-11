# Mini-ADR: Implement Due Dates, Overdue Filter, and Task Comments

## Status

Accepted

## Context

The Module 1 Task Tracker is a learning project with a Python/FastAPI backend, Pydantic validation, local JSON file storage, and a separate simple web frontend. The goal is to add two small, scoped features using an AI-assisted workflow while keeping the design easy to understand, test, and run locally.

Selected features:

1. Due dates + overdue filter
2. Task comments

The project is not production software. Authentication, user accounts, admin roles, notifications, mobile-specific behavior, real-time updates, Docker, cloud deployment, and microservices are out of scope.

## Decision

The two features will be implemented with small changes to the existing task model, API routes, storage logic, frontend form, task cards, and tests.

## Feature 1: Due Dates + Overdue Filter

Tasks will support an optional `due_date` field.

Design decisions:

- `due_date` will be optional.
- The backend will validate the date using Pydantic.
- The expected date format will be ISO date format: `YYYY-MM-DD`.
- Tasks without a due date remain valid.
- A task is overdue when:
  - it has a due date before today, and
  - its status is not `Done`.
- The frontend will show the due date on task cards when present.
- The frontend will show an overdue pill or visual indicator for overdue tasks.
- The task list will support an overdue filter.

The overdue calculation can be done in the backend or frontend. For this project, the main API/storage logic should treat overdue as a derived value instead of permanently storing it. This avoids stale data if the date changes.

## Feature 2: Task Comments

Tasks will support simple comments stored directly inside each task.

Design decisions:

- Each task will have a `comments` list.
- A comment will contain simple text.
- Blank or whitespace-only comments will be rejected.
- Comments will be stored with the task in the JSON file.
- Comments will be displayed in the edit modal or task detail area.
- Task cards may show a comment count.
- Adding a comment to a missing task returns `HTTP 404`.

For this learning project, comments support add and delete operations only. They do not need authors, timestamps, editing, threading, or separate comment ownership.

## Alternatives Suggested by AI

AI suggested or implied several possible implementation options:

1. Store tasks in SQLite instead of JSON.
2. Use a separate comments table or separate comments API resource.
3. Store an `is_overdue` field directly on each task.
4. Add richer comment metadata such as author, timestamp, edited status, or delete support.
5. Build a more advanced frontend state management layer.

## Rejected Alternatives

The following alternatives were rejected as too complex or out of scope:

### SQLite or SQLModel Storage

Rejected because the project previously chose the simpler JSON file architecture. SQLite would be more realistic, but it would introduce database sessions, schema setup, and more testing complexity.

### Separate Comments Table or Comments Service

Rejected because there is no database and the comments feature is intentionally small. Storing comments directly inside each task is simpler and easier to understand.

### Persisting `is_overdue` as a Stored Field

Rejected because overdue status changes over time. Storing it directly could become incorrect unless it is recalculated regularly. It is better to compute overdue from `due_date` and `status`.

### Comment Authors, Timestamps, Editing, and Deleting

Rejected because the project has no authentication or user accounts, and the selected feature only requires simple text comments with basic add/delete behavior. Rich metadata and editing would expand the feature beyond the required learning scope.

### Real-Time Comment Updates

Rejected because real-time updates are explicitly out of scope. The frontend only needs to refresh the task data after a comment is added.

## Consequences

### Positive Consequences

- The design stays small and understandable.
- The backend remains easy to test with pytest and TestClient.
- The frontend changes are visible and useful.
- Both features are easy to explain in the AI workflow log.
- The JSON storage approach remains consistent with the accepted architecture.

### Negative Consequences

- Comments are basic and do not support authorship metadata, timestamps, or editing.
- JSON storage is not ideal for concurrent writes.
- Overdue behavior depends on consistent date handling.
- More advanced filtering or reporting would be easier with a database.

## Final Decision

Implement due dates, overdue filtering, and task comments as small extensions to the existing JSON-backed task model and REST API. Keep the implementation focused on validation, task display, filtering, and basic add/delete comments. Avoid database migration, authentication, real-time features, or advanced comment functionality.
