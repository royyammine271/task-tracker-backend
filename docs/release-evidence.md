# Release Evidence

## B1. Continuous Integration

- Workflow file: [.github/workflows/ci.yml](../.github/workflows/ci.yml)
- Trigger: push and pull_request
- Install step: `python -m pip install --upgrade pip` and `pip install -r requirements.txt`
- Test step: `pytest -v`
- Safety check: no `continue-on-error`, no `|| true`, no skipped pytest command, and Python is pinned to `3.11`.
- Local equivalent result: `35 passed, 3 warnings in 0.51s`
- GitHub Actions link: not available from this local environment; the workflow file is present and the equivalent local run passed.

## B2. Docker and runtime verification

- Dockerfile exists at [Dockerfile](../Dockerfile) and .dockerignore exists at [.dockerignore](../.dockerignore).
- Build command used:
  ```powershell
  docker build -t task-tracker:release .
  ```
- Run command used:
  ```powershell
  docker run --rm -d --name task-tracker-verify -p 8010:8000 task-tracker:release
  ```
- Health check used:
  ```powershell
  Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8010/health
  ```
- Result: HTTP 200 OK with body `{"status":"ok","timestamp":"2026-08-12T11:06:48.101051+00:00"}`
- Docker safety check: the image runs as a non-root user (`USER app`), `.env` files are excluded by `.dockerignore`, and the runtime command is `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

## B3. Documentation checked against reality

The repo already contains the required setup and verification commands in [README.md](../README.md). The following checks were verified against the actual repo or running app:

1. `CI runs on push and pull_request` — confirmed by [.github/workflows/ci.yml](../.github/workflows/ci.yml).
2. `GET /health returns HTTP 200` — confirmed by both the local app and the containerized app.
3. `Docker runs uvicorn on port 8000` — confirmed by the container log: `Uvicorn running on http://0.0.0.0:8000`.
4. `The project uses Python 3.11 in CI and Docker` — confirmed by the workflow and Dockerfile.

## Verified baseline summary

- Branch: final-project
- Local app command: `./.venv/Scripts/uvicorn app.main:app --host 127.0.0.1 --port 8003`
- Test command: `./.venv/Scripts/python.exe -m pytest -q`
- Result: `35 passed, 3 warnings in 0.51s`
- No application code changes were made during this release check.
