# Release Evidence

## Baseline
- Branch: final-project
- Date: 2026-08-12
- Local app run command: `./.venv/Scripts/uvicorn app.main:app --host 127.0.0.1 --port 8003`
- /health result: HTTP 200 OK, JSON payload `{"status":"ok","timestamp":"2026-08-12T11:00:16.784040+00:00"}`
- Frontend check: opened [frontend/index.html](../frontend/index.html); the Kanban board and task cards remained visible, including the New Task action and Edit buttons.
- Test command: `./.venv/Scripts/python.exe -m pytest -q`
- Test result: `35 passed, 3 warnings in 0.51s`

## CI evidence
- Workflow file: [.github/workflows/ci.yml](../.github/workflows/ci.yml)
- Latest green run link: https://github.com/royyammine271/task-tracker-backend/actions/runs/31603794921
- Workflow run note: CI #9 completed successfully for commit `7d793fe` on branch `final-project` (run shown on the CI workflow page).
- Test command used by CI: `pytest -v`
- Shortcut check: no continue-on-error / no `|| true` / pytest is not skipped.

## Docker evidence
- Build command: `docker build -t task-tracker:release .`
- Run command: `docker run --rm -d --name task-tracker-verify -p 8010:8000 task-tracker:release`
- /health check: `Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8010/health`
- Non-root check, if implemented: `USER app` is set in [Dockerfile](../Dockerfile).
- No-baked-secrets check: [.dockerignore](../.dockerignore) excludes `.env` and `.env.*` from build context.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| CI runs on push and pull_request | [.github/workflows/ci.yml](../.github/workflows/ci.yml) | Matched | No change |
| GET /health returns HTTP 200 | Local app run and Docker run responses | Matched | No change |
| Docker runs uvicorn on port 8000 | Docker logs from container run | Matched | No change |
| README commands reflect the verified workflow | [README.md](../README.md), actual run commands, Docker health result | Needed minor wording cleanup | Updated README to match the verified commands and output |

## Notes
- The warnings are dependency deprecations from FastAPI/Starlette and are not failing test results.
- No application code changes were made during this release verification.
