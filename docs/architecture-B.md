# Architecture B - Task Tracker

## 1. What the app does
Task Tracker is a learning-project application that lets users create, view, update, filter, and delete tasks on a board, including status movement and task comments, with a FastAPI backend serving JSON endpoints and a vanilla JavaScript frontend consuming those endpoints.

## 2. Data model
- Task
  - id: string UUID
  - title: required string, trimmed, non-blank, max 200
  - description: string (default empty)
  - status: enum (ToDo, InProgress, Done)
  - priority: enum (Low, Medium, High)
  - assignee: optional string
  - due_date: optional date (YYYY-MM-DD)
  - comments: list of strings
  - created_at: UTC datetime
  - updated_at: UTC datetime
- Comment create payload (current)
  - comment: required string, trimmed, non-blank

## 3. Request flow (create task)
1. The frontend collects modal form input and sends POST /tasks with JSON.
2. The backend route validates the payload against TaskCreate rules.
3. The storage layer generates id and UTC timestamps, builds the task object, persists it to JSON storage, and returns it.
4. The API responds with HTTP 201 and the created task.
5. The frontend refreshes task data from GET /tasks and re-renders the board.

## 4. Key files
- [AGENTS.md](AGENTS.md): project scope, stack, and verified conventions for this repo.
- [app/main.py](app/main.py): API entrypoint, route definitions, and HTTP error mapping.
- [app/models.py](app/models.py): enums, request/response models, and field validators.
- [app/storage.py](app/storage.py): JSON persistence and task/comment mutation logic.
- [app/business_rules.py](app/business_rules.py): task status transition validation rules.
- [app/schemas.py](app/schemas.py): shared API schema objects (for example health response).
- [frontend/index.html](frontend/index.html): single-file UI, fetch calls, modal actions, drag/drop, and comment interactions.
- [tests/test_tasks.py](tests/test_tasks.py): integration-style API behavior tests.
- [tests/conftest.py](tests/conftest.py): fixtures and per-test storage reset behavior.
- [README.md](README.md): run commands, route summary, and project conventions.

## 5. Conventions
- Validation
  - Input validation is model-driven (required fields, enums, date parsing, and unknown-field rejection).
- Storage
  - Data is persisted as JSON in a file-backed store; mutations rewrite stored task state.
- Error handling
  - Missing resources return 404 with detail text; invalid transitions and invalid payloads return 422.
- Frontend/backend interaction
  - Frontend uses fetch-based JSON calls and refreshes or updates in-memory board state after write operations.

## 6. Not visible or assumptions
- No authentication/authorization mechanism is visible in inspected backend routes.
- No database or migration framework is visible; persistence appears file-based.
- Deployment topology and production infrastructure are not confirmed by the inspected files.
- Assumption: comments are intentionally represented as string list items in the current model, because models, storage logic, frontend rendering, and tests all align on that shape.
