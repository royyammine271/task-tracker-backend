# Architecture C - Task Tracker (Targeted Context)

## 1. What the app does
Task Tracker is a backend API that manages tasks and task comments: it supports health checks, creating/listing/getting/updating/deleting tasks, filtering tasks by status/priority/overdue, and adding/removing comments on tasks, with data persisted in a JSON-backed storage layer.

## 2. Data model
- TaskStatus enum: ToDo, InProgress, Done.
- TaskPriority enum: Low, Medium, High.
- TaskCreate: title, description, status, priority, assignee, due_date.
- TaskUpdate: optional partial fields for title/description/status/priority/assignee/due_date.
- TaskResponse: id, title, description, status, priority, assignee, due_date, comments (list of strings), created_at, updated_at.
- TaskCommentCreate: comment (single required string).

## 3. Request flow (create task)
1. Client sends POST /tasks with a TaskCreate-compatible JSON body.
2. Route handler in app/main.py validates payload through TaskCreate and forwards to storage.add_task.
3. Storage generates UUID + UTC timestamps, builds a TaskResponse object, stores it in memory map, and writes the full map to JSON file.
4. API returns HTTP 201 with the created TaskResponse payload.

## 4. Key files
- [app/main.py](app/main.py): API entrypoint, route definitions, response codes, and HTTP error mapping.
- [app/models.py](app/models.py): enums, request/response models, and field validators.
- [app/storage.py](app/storage.py): JSON persistence, filtering, and mutation logic.
- [app/business_rules.py](app/business_rules.py): imported transition validator used by storage; internals not visible from the files I read.
- [app/schemas.py](app/schemas.py): imported health response model used by /health; internals not visible from the files I read.

## 5. Conventions
- Validation
  - Pydantic model validators enforce trimmed non-blank title/comment and due_date parsing; unknown fields are forbidden.
- Storage
  - Data source path is TASKS_DATA_FILE env var or app/tasks.json default; storage reloads from file and rewrites on mutations.
- Error handling
  - 404 is returned for missing tasks/comments in route handlers; invalid model input returns 422 via validation; invalid status transition behavior depends on app/business_rules.py and is not visible from the files I read.
- Frontend/backend interaction
  - Not visible from the files I read.

## 6. Not visible or assumptions
- Frontend structure, request timing, and UI behavior are not visible from the files I read.
- Test coverage and naming conventions are not visible from the files I read.
- Exact shape of HealthResponse is not visible from the files I read.
- Exact status transition rule table is not visible from the files I read.
- Assumption: the persistence file is JSON text compatible with TaskResponse model_dump serialization.
