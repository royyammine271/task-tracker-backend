# Task Tracker Backend

A lightweight FastAPI backend for a Task Tracker project with a vanilla JS frontend and JSON file storage.

## Features

### Backend

- Health endpoint: `GET /health`
- Task CRUD endpoints:
  - `POST /tasks`
  - `GET /tasks`
  - `GET /tasks/{task_id}`
  - `PATCH /tasks/{task_id}`
  - `DELETE /tasks/{task_id}`
- Task comments:
  - `POST /tasks/{task_id}/comments`
  - `DELETE /tasks/{task_id}/comments/{comment_index}`
  - Comments are stored per task as a list of strings
  - Blank or whitespace-only comments return `422`
  - Missing task IDs return `404`
- Workflow rules for status transitions:
  - `ToDo -> InProgress`
  - `InProgress -> Done`
  - `Done -> InProgress`
- Optional filtering on list endpoint:
  - by `status`
  - by `priority`
  - by `overdue`

### Frontend

- Kanban board with three columns: To Do, In Progress, Done
- Drag-and-drop status movement that follows backend transition rules
- Task creation and editing modal (title, description, status, priority, due date, assignee)
- Comments section in edit modal:
  - View existing comments
  - Add a new comment
  - Delete an existing comment
  - Inline validation/error messages
- Comment count displayed on each task card
- Overdue filter toggle

## Setup

### 1. Create and activate a virtual environment

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example env file and adjust values if needed:

**Linux / macOS:**
```bash
cp .env.example .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

## Running the server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Open the frontend

Open `frontend/index.html` in a browser (for example with VS Code Live Server or by opening the file directly).

If your backend runs on a different host or port, update the `BASE_URL` in `frontend/index.html`.

## Run tests

```bash
pytest -q
```

## Testing the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "ok", "timestamp": "2026-07-04T12:00:00.000000+00:00"}
```
