# Module 4 Task Tracker

## Final Project Status

This repository is a small learning project and is intentionally kept within scope. It is a FastAPI backend with JSON storage, a simple frontend, and a narrow set of task-tracking behaviors. No new product features were added in the final project pass; the aim was to confirm the app still works, document the release checks, and explain how AI was used responsibly.

### Scope confirmation
- The project remains limited to task CRUD, status transitions, optional due dates, and the existing frontend workflow.
- It does not add authentication, a production database, notifications, or unrelated UI redesign.
- The accepted design is documented in [docs/mini-adr.md](docs/mini-adr.md) and the evidence trail is in [docs/prompt-log.md](docs/prompt-log.md), [docs/reflection.md](docs/reflection.md), and [docs/verification.md](docs/verification.md).

### Release baseline
The current verified baseline from this repo is:
- Branch: `final-project`
- Test command: `./.venv/Scripts/python.exe -m pytest -q`
- Result: `35 passed, 3 warnings in 0.60s`
- Runtime check: `curl http://127.0.0.1:8002/health`
- Result: HTTP 200 with a JSON status payload

### Release checks to use before handoff
1. Run the backend test suite: `./.venv/Scripts/python.exe -m pytest -q`
2. Start the app: `./.venv/Scripts/uvicorn app.main:app --host 127.0.0.1 --port 8000`
3. Confirm the health endpoint returns HTTP 200: `http://127.0.0.1:8000/health`
4. Keep the repo within original project scope and do not add unrelated features
5. If Docker is available, run: `docker build -t task-tracker:dev .` and `docker run --rm -p 8000:8000 task-tracker:dev`

## 1) Project Overview

This repository contains a Module 4 Task Tracker built with FastAPI and Pydantic, with JSON file storage and a vanilla JavaScript frontend board.

Current backend API routes are implemented in [app/main.py](app/main.py):
- GET /health
- POST /tasks
- GET /tasks
- GET /tasks/{task_id}
- PATCH /tasks/{task_id}
- DELETE /tasks/{task_id}
- POST /tasks/{task_id}/comments
- DELETE /tasks/{task_id}/comments/{comment_index}

The frontend is in [frontend/index.html](frontend/index.html) and includes drag-and-drop status movement, due date display/filtering, and comments UI.

## 2) Prerequisites

- Python 3.11 recommended for Module 4 parity with CI and Docker.
- pip
- Git
- Docker Desktop (optional, for container run)

[VERIFY] Local development may work on Python versions other than 3.11, but CI and Docker are pinned to 3.11.

## 3) Local Setup

From repository root:

Windows PowerShell:
1. python -m venv .venv
2. .\.venv\Scripts\Activate.ps1
3. python -m pip install --upgrade pip
4. pip install -r requirements.txt
5. Copy-Item .env.example .env

Linux/macOS:
1. python3 -m venv .venv
2. source .venv/bin/activate
3. python -m pip install --upgrade pip
4. pip install -r requirements.txt
5. cp .env.example .env

## 4) Run the App Locally

From repository root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

API base URL:
- http://127.0.0.1:8000

Quick health check:
- curl http://127.0.0.1:8000/health

PowerShell health check:
- (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health).Content

Verified local result in this environment:
- Health endpoint responded with HTTP 200 on port 8003 when a free port was used, which matches the app's `/health` behavior.

## 5) Run Tests

From repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Verified local result:
- 35 passed, 3 warnings in 0.51s

## 6) Run with Docker

From repository root:

```powershell
docker build -t task-tracker:release .
docker run --rm -d --name task-tracker-verify -p 8010:8000 task-tracker:release
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8010/health
```

Verified local result:
- HTTP 200 OK from the containerized app on port 8010.

Stop container:
- docker rm -f task-tracker-verify

## 7) CI Workflow Summary

CI workflow file: [.github/workflows/ci.yml](.github/workflows/ci.yml)

What it does:
- Triggers on push and pull_request
- Uses actions/checkout
- Uses actions/setup-python with Python 3.11
- Installs dependencies from [requirements.txt](requirements.txt)
- Runs pytest -v

This module CI does not include deployment steps.

## 8) Project Structure

task-tracker-backend/
- app/
  - main.py
  - models.py
  - storage.py
  - business_rules.py
  - schemas.py
- tests/
  - test_tasks.py
  - conftest.py
- frontend/
  - index.html
- docs/
  - ai-playbook.md
  - final-ai-review.md
  - release-evidence.md
  - mini-adr.md
  - verification.md
- requirements.txt
- Dockerfile
- .dockerignore
- .github/workflows/ci.yml
- AGENTS.md

## 9) AI Usage and Human Review

This project includes a documented AI review trail. The evidence is in [docs/prompt-log.md](docs/prompt-log.md), [docs/reflection.md](docs/reflection.md), [docs/verification.md](docs/verification.md), and [docs/final-ai-review.md](docs/final-ai-review.md).

The key rule was simple: AI output was treated as an initial draft, not an unquestioned source of truth. Any suggestion that widened scope, added unsupported features, or ignored the project guardrails was reviewed and either edited or rejected.

## 10) Project Conventions and Current Limitations

Conventions:
- Keep changes small and scoped.
- Preserve existing API contract unless explicitly requested.
- Keep endpoint and error response style consistent.
- Update docs when behavior changes.

Current limitations (intentional for final project):
- No authentication or user accounts
- No database (JSON file storage only)
- No deployment pipeline beyond the course CI example
- Not production-hardened (learning project scope)

## 11) Technical Notes and Decisions

Technical decision notes:
- [docs/mini-adr.md](docs/mini-adr.md)
- [docs/ai-playbook.md](docs/ai-playbook.md)

Verification notes:
- [docs/verification.md](docs/verification.md)
- [docs/release-evidence.md](docs/release-evidence.md)
