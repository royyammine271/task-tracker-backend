# AGENTS.md

## Project Summary
This repository contains the Task Tracker backend and frontend used in course modules.
Backend: FastAPI app with JSON-file persistence.
Frontend: vanilla JavaScript board UI with task editing, comments, and status movement.
Current API entrypoint: [app/main.py](app/main.py).
Current persistence layer: [app/storage.py](app/storage.py).

## Tech Stack
- Python
- FastAPI
- Pydantic
- Uvicorn
- Pytest
- python-dotenv
- httpx (test client support)
- Vanilla HTML/CSS/JS frontend

Evidence:
- Dependencies in [requirements.txt](requirements.txt)
- Routes in [app/main.py](app/main.py)
- Frontend in [frontend/index.html](frontend/index.html)

## Confirmed Run and Test Commands
Run app locally from repo root:
- uvicorn app.main:app --reload --port 8000

Run tests from repo root:
- pytest -v

Also seen in repo:
- CI test command is pytest -v in [.github/workflows/ci.yml](.github/workflows/ci.yml)
- [CLAUDE.md](CLAUDE.md) suggests python -m pytest -q as a workflow command

If commands differ by environment, treat as not confirmed until reproduced locally.

## Business Rules Visible in Code

### Task Status Values
- ToDo
- InProgress
- Done
Source: [app/models.py](app/models.py)

### Task Priority Values
- Low
- Medium
- High
Source: [app/models.py](app/models.py)

### Status Transition Rules
Allowed:
- ToDo -> InProgress
- InProgress -> Done
- Done -> InProgress
Invalid transitions raise HTTP 422.
Source: [app/business_rules.py](app/business_rules.py)

### Validation Rules
- title is required, trimmed, non-blank, max length 200
- due_date accepts None, date object, or YYYY-MM-DD string
- comment is required, trimmed, non-blank
- unknown fields in request models are forbidden
Source: [app/models.py](app/models.py)

### Overdue Logic
A task is overdue only when:
- status is not Done
- due_date is set
- due_date is earlier than today
Source: [app/storage.py](app/storage.py)

### Response Behavior Confirmed in Routes
- POST /tasks returns 201
- DELETE /tasks/{task_id} returns 204
- Missing task for get/patch/delete/comment operations returns 404
Source: [app/main.py](app/main.py)

## Module 5 Guardrails
1. Docs-first:
- Read [README.md](README.md), [CLAUDE.md](CLAUDE.md), and relevant docs before proposing edits.
- Confirm requirements and acceptance criteria in writing before code changes.

2. Read-only by default:
- Start with analysis, evidence gathering, and plan.
- Do not edit unless explicitly approved.

3. One task per thread:
- Keep each thread focused on one concrete task.
- If a new task appears, summarize and open a separate thread/step.

4. No app changes without explicit approval:
- Do not modify files under [app](app) unless the user explicitly approves app code changes.
- If app changes are requested implicitly, ask for explicit approval first.

## Security and Governance Reminders
- Do not paste, expose, or commit secrets (.env values, tokens, credentials).
- Do not run destructive commands (example: hard reset, force-delete) unless explicitly requested.
- Cite files for every technical claim.
- Do not invent findings; if uncertain, label as not confirmed.
- Keep changes minimal and scoped to the requested task.
- Preserve existing API contracts unless a change is explicitly requested and documented.

## Working Agreement for This Repo
- Verify current branch and repo state before edits.
- Prefer small, reviewable changes.
- Update docs when behavior changes.
- Run targeted verification appropriate to the change.
