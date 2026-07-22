# Verification Report

Date: 2026-07-22
Project: Task Tracker backend/frontend (FastAPI + Pydantic + JSON storage + vanilla JS)

## 1) Baseline Check

Source: baseline-pytest-result.txt

Observed baseline output snapshot:
- Platform: win32, Python 3.14.0
- Collected: 19 tests
- Result: 17 passed, 2 failed
- Failing tests in baseline:
  - tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
  - tests/test_tasks.py::test_patch_same_status_returns_422

Note:
- The baseline file appears to be an older run snapshot (UTF-16 encoded) and does not include the newer comments tests.

## 2) Backend Test Results (Current)

Command used:
- & "c:/Users/royya/Desktop/AI Assisted Coding Certificate/Task-Tracker/task-tracker-backend/.venv-1/Scripts/python.exe" -m pytest -q

Current result:
- 32 passed, 0 failed
- Warnings: 3 (deprecation warnings only)

Coverage relevant to task comments (from tests/test_tasks.py):
- Add comment to existing task succeeds and response includes new comment.
- Blank comment (empty string) returns 422.
- Whitespace-only comment returns 422.
- Missing task on add comment returns 404.
- Comments remain attached to the correct task.
- Existing JSON tasks without comments load with comments defaulting to [].
- Returned task includes accurate comments list/count semantics (list content and length assertions).

## 3) Manual Browser Checks

Environment used:
- Frontend opened directly: file:///.../frontend/index.html
- Backend API target in UI: http://127.0.0.1:8001

Checks performed and results:
1. Load board page
- Result: PASS
- Board rendered with 3 columns and zero tasks initially.

2. Create task from modal
- Action: Click New Task, enter title "Verification Task", save.
- Result: PASS
- Task appears in To Do column.

3. Comment count on card before comment
- Result: PASS
- Card shows "Comments 0".

4. Add valid comment in Edit modal
- Action: Open Edit, add comment "Looks good", submit.
- Result: PASS
- Comment appears in comments list.
- Card updates to "Comments 1".

5. Add blank/whitespace comment
- Action: Submit empty/whitespace comment from same modal.
- Result: PASS
- UI shows validation error: "Comment is required".
- No extra comment added.

## 4) Behavior Contract Before/After Refactor

### Before (pre-comments feature)
- Task shape included:
  - id, title, description, status, priority, assignee, due_date, created_at, updated_at
- Endpoints included:
  - POST /tasks
  - GET /tasks
  - GET /tasks/{task_id}
  - PATCH /tasks/{task_id}
  - DELETE /tasks/{task_id}
- No task comments field or comment-specific endpoint.

### After (comments feature)
- Task shape now includes:
  - comments: list[str] (defaults to [] for new and legacy tasks)
- New request model:
  - comment payload with required non-blank/trimmed text
- New endpoint:
  - POST /tasks/{task_id}/comments
- Contract behavior:
  - 200 and updated task body on success
  - 422 for blank/whitespace-only comment
  - 404 if task_id does not exist
- Storage behavior:
  - Uses existing JSON file storage
  - Comment persists on the correct task record

## 5) Break Test Evidence (2+ tests)

Purpose:
- Demonstrate that tests fail when key comment behavior is intentionally broken.
- Temporary regressions were introduced and then reverted immediately.

### Break Evidence A: Remove whitespace trimming in comment validator
Temporary regression:
- In app/models.py, removed strip() before blank check.

Focused tests run:
- pytest -q tests/test_tasks.py -k "add_comment_blank_returns_422 or add_comment_empty_string_returns_422"

Observed result:
- 1 failed, 1 passed
- Failure:
  - test_add_comment_blank_returns_422 expected 422, got 200

Interpretation:
- Test correctly catches regression where whitespace-only comments are wrongly accepted.

### Break Evidence B: Overwrite comments list instead of appending
Temporary regression:
- In app/storage.py, changed comment update from append behavior to replacement ([comment]).

Focused tests run:
- pytest -q tests/test_tasks.py -k "comment_count_updates_when_multiple_comments_added or comments_stay_attached_to_correct_task"

Observed result:
- 1 failed, 1 passed
- Failure:
  - test_comment_count_updates_when_multiple_comments_added expected length 2, got 1

Interpretation:
- Test correctly catches regression where the second comment replaces the first instead of accumulating.

### Post-break restoration check
Final confirmation command:
- & "c:/Users/royya/Desktop/AI Assisted Coding Certificate/Task-Tracker/task-tracker-backend/.venv-1/Scripts/python.exe" -m pytest -q

Result after restoring temporary breaks:
- 32 passed, 0 failed

## 6) Conclusion

- Comments feature behavior is verified by automated tests and manual browser checks.
- Backward compatibility for legacy tasks without comments is verified.
- Break-test exercises demonstrate that core comments tests detect realistic regressions.
