# Module 4 Task Tracker

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

uvicorn app.main:app --reload --port 8000

API base URL:
- http://127.0.0.1:8000

Quick health check:
- curl http://127.0.0.1:8000/health

PowerShell health check:
- (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health).Content

## 5) Run Tests

Course command from repository root:

pytest -v

## 6) Run with Docker

From repository root:

1. docker build -t task-tracker:dev .
2. docker run -d --name tt-dev -p 8000:8000 task-tracker:dev
3. docker ps --filter "name=^tt-dev$"
4. curl http://127.0.0.1:8000/health

PowerShell health check:
- (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health).StatusCode

Stop while keeping the container:
- docker stop tt-dev

Start again:
- docker start tt-dev

Remove when done:
- docker rm -f tt-dev

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
  - ci-workflow-decision-note.md
  - mini-adr.md
  - verification.md
- requirements.txt
- Dockerfile
- .dockerignore
- .github/workflows/ci.yml
- CLAUDE.md

## 9) Project Conventions and Current Limitations

Conventions:
- Keep changes small and scoped.
- Preserve existing API contract unless explicitly requested.
- Keep endpoint and error response style consistent.
- Update docs when behavior changes.

Current limitations (intentional for Module 4):
- No authentication or user accounts
- No database (JSON file storage only)
- No deployment pipeline in this module
- Not production-hardened (learning project scope)

## 10) Technical Notes and Decisions

Technical decision notes:
- [docs/ci-workflow-decision-note.md](docs/ci-workflow-decision-note.md)
- [docs/mini-adr.md](docs/mini-adr.md)

Verification notes:
- [docs/verification.md](docs/verification.md)
