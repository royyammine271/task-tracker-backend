# CLAUDE.md

Project: Task Tracker Backend (Module 4)
Stack: FastAPI, Pydantic, JSON storage, vanilla JS frontend

## 1) Working Agreement

- Always confirm current branch before edits.
- Prefer small, scoped changes over large refactors.
- Do not modify unrelated files.
- Keep API contracts backward compatible unless explicitly requested.
- Explain planned changes before applying them.

## 2) Safety Rules

- Do not run destructive Git commands unless explicitly asked.
- Never remove tests to make failures pass.
- Do not overwrite documentation with guessed values.
- If assumptions are needed, state them clearly first.
- If repository state is unexpected, stop and ask before proceeding.

## 3) Repository Orientation (Read First)

1. README.md
2. app/main.py
3. app/models.py
4. app/storage.py
5. frontend/index.html
6. tests/test_tasks.py

## 4) Coding Preferences

- Keep naming and style consistent with existing files.
- Add brief comments only where logic is non-obvious.
- Preserve current endpoint patterns and error response style.
- Keep changes easy to review and explain in class artifacts.

## 5) Verification Workflow

Before coding:
- Confirm branch and sync state:
  - git rev-parse --abbrev-ref HEAD
  - git status -sb

After coding:
- Run targeted tests first, then full suite.
- For backend changes, validate related endpoint behavior.
- For frontend changes, do a quick manual browser check.

Suggested test command:
- python -m pytest -q

## 6) Documentation Discipline

When behavior changes, update related docs in the same branch:
- docs/midcourse/mini-adr.md
- docs/midcourse/verification.md

Do not leave stale metrics or contradictory claims.

## 7) Commit and Push Discipline

- Commit message format:
  - feat: ...
  - fix: ...
  - docs: ...
  - chore: ...
- Push only after checks pass and docs are aligned.
- Confirm remote branch head after push.

## 8) Manual UX Checks (Frontend)

- Create task from modal.
- Drag/drop valid status transitions.
- Confirm invalid transitions are blocked.
- Verify due date and overdue filter behavior.
- Add and delete comments; verify count updates.
- Refresh page and confirm persistence.

## 9) If Claude CLI Is Not Installed

If `claude` command is missing in PowerShell, install via:

- irm https://claude.ai/install.ps1 | iex

Then verify:

- claude --version

Start in repo root:

- claude
