# Architecture A - Task Tracker

## 1. What the app does
Task Tracker is a course project web app for creating, viewing, updating, filtering, and deleting tasks on a simple board, with status transitions, due-date handling, and task comments; a FastAPI backend exposes JSON endpoints, and a single-page vanilla JavaScript frontend calls those endpoints and renders the UI.

## 2. Data model
- Task
  - id: string UUID
  - title: required string (trimmed, non-blank, max 200)
  - description: string (defaults to empty)
  - status: enum (ToDo, InProgress, Done)
  - priority: enum (Low, Medium, High)
  - assignee: optional string
  - due_date: optional date (YYYY-MM-DD)
  - comments: list of strings
  - created_at: UTC datetime
  - updated_at: UTC datetime
- Comment input (current implementation)
  - comment: required string (trimmed, non-blank)

## 3. Request flow (create task)
1. Frontend builds a JSON payload from the task modal and sends POST /tasks.
2. FastAPI route in main receives payload and validates with Pydantic TaskCreate rules.
3. Storage layer generates task id and UTC timestamps, builds TaskResponse, and writes full task map to tasks.json.
4. API returns 201 with created task JSON.
5. Frontend refreshes task list via GET /tasks and re-renders board columns.

## 4. Key files
- [app/main.py](app/main.py): FastAPI app setup, CORS policy, and route handlers.
- [app/models.py](app/models.py): Pydantic models, enums, and field validators.
- [app/storage.py](app/storage.py): JSON-file persistence, load/save, CRUD, and comment mutation.
- [app/business_rules.py](app/business_rules.py): status transition rules and 422 error for invalid moves.
- [app/schemas.py](app/schemas.py): shared response schema(s) such as health response.
- [frontend/index.html](frontend/index.html): full frontend UI, modal logic, fetch calls, board rendering, and comments UI.
- [tests/test_tasks.py](tests/test_tasks.py): API and behavior tests for tasks, filters, transitions, and comments.
- [tests/conftest.py](tests/conftest.py): pytest fixtures and per-test storage reset.
- [README.md](README.md): run/test commands and documented route surface.

## 5. Conventions
- Validation
  - Pydantic models enforce required fields, enum values, due date parsing, and unknown-field rejection via extra=forbid.
- Storage
  - Backend persists all tasks in one JSON file, reloads on read paths, and rewrites on mutation.
- Error handling
  - Missing task/comment paths return 404 with detail strings; invalid status transitions return 422; model validation errors also return 422.
- Frontend/backend interaction
  - Frontend uses fetch to call REST endpoints, sends/receives JSON, and refreshes in-memory board state after writes.

## 6. Not visible or assumptions
- No authentication or authorization flow is visible in current backend routes.
- No database migrations are visible; persistence is file-based JSON.
- No production deployment topology is confirmed from code alone (only local/CI run conventions are visible).
- Assumption: comments are intentionally modeled as plain strings today (not structured comment objects) because both models and tests assert that shape.
