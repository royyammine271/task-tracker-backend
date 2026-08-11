# Comments Feature Plan (Repo-Grounded, Read-Only)

## 1) Data Model

### Current pattern observed
- Request/response models are centralized in [app/models.py](app/models.py).
- API route handlers depend on those models in [app/main.py](app/main.py).
- Persisted task shape currently includes comments as a list of strings in [app/models.py](app/models.py) and [app/storage.py](app/storage.py).

### Planned model changes
- Add a dedicated comment response model in [app/models.py](app/models.py) with:
  - id: UUID as string
  - task_id: string task reference
  - author: required string, length 1-100
  - body: required string, length 1-2000
  - created_at: server-generated UTC datetime
- Add a dedicated create-comment request model in [app/models.py](app/models.py):
  - author
  - body
  - No client-supplied id or created_at.
- Update task response shape so comments becomes a list of comment objects instead of a list of strings.
- Keep existing model conventions:
  - unknown fields forbidden
  - field-level validators for trimming and length checks

### Why this fits existing conventions
- This repo uses strict input validation and explicit response models in [app/models.py](app/models.py).
- Existing comments behavior is task-scoped and returned via task payloads in [app/main.py](app/main.py), so adding structure to comments aligns with current API style rather than introducing a separate complex subsystem immediately.

## 2) API Routes

### Current pattern observed
- Task-scoped comments already exist:
  - POST /tasks/{task_id}/comments
  - DELETE /tasks/{task_id}/comments/{comment_index}
- Missing task returns 404 with consistent detail message style in [app/main.py](app/main.py).
- Current delete is index-based, not id-based.

### Planned route design
1. Create comment
- Method/path: POST /tasks/{task_id}/comments
- Request body: author, body
- Response body: updated task object (to preserve current frontend update flow), with comments as structured objects
- Error cases:
  - 404 if task not found
  - 422 for validation failures (blank, too long, missing)

2. Delete comment by comment id (recommended)
- Method/path: DELETE /tasks/{task_id}/comments/{comment_id}
- Response body: updated task object (consistent with current frontend pattern that re-renders task + board)
- Error cases:
  - 404 if task not found
  - 404 if comment id not found for that task

3. Compatibility note
- Existing frontend calls index-based delete in [frontend/index.html](frontend/index.html).
- Team should decide if index route is:
  - replaced, or
  - temporarily supported in parallel during migration.

## 3) Tests

### Current style observed
- Test naming is descriptive and scenario-oriented in [tests/test_tasks.py](tests/test_tasks.py).
- Assertions check status code plus full/partial JSON shape.
- Existing comments tests already cover add/delete behavior for string comments.

### Proposed concrete test names

### Happy path
- test_add_structured_comment_returns_200_and_comment_fields
- test_add_multiple_structured_comments_preserves_order
- test_delete_comment_by_id_removes_only_target_comment
- test_comment_created_at_is_server_generated_utc
- test_comment_id_is_uuid_string
- test_comments_stay_attached_to_correct_task_with_structured_shape

### Validation
- test_add_comment_missing_author_returns_422
- test_add_comment_blank_author_returns_422
- test_add_comment_author_over_100_returns_422
- test_add_comment_missing_body_returns_422
- test_add_comment_blank_body_returns_422
- test_add_comment_body_over_2000_returns_422
- test_add_comment_unknown_field_returns_422
- test_add_comment_client_supplied_created_at_rejected_or_ignored_per_contract

### Edge cases
- test_add_comment_missing_task_returns_404
- test_delete_comment_by_id_missing_task_returns_404
- test_delete_comment_by_id_not_found_returns_404
- test_storage_loads_legacy_string_comments_and_normalizes_shape
- test_mixed_legacy_and_new_comments_serialize_consistently

## 4) Frontend Changes

### Current behavior observed
- Comment UI is in [frontend/index.html](frontend/index.html).
- Add comment currently sends body with one field named comment.
- Delete comment currently uses array index.
- Rendering expects each comment to be plain text and shows comment count.

### Planned frontend updates
- Update modal comment form to capture:
  - author
  - body
- Update add-comment request payload to match new API contract.
- Update comment rendering:
  - show author + body + created_at
  - keep existing comment count behavior
- Update delete handler to use comment id (if backend route changes to id-based).
- Keep current UX error handling pattern:
  - field-level error display
  - non-200 handling from API and message surfacing

### Files likely to change
- [frontend/index.html](frontend/index.html) (current app is single-file HTML/CSS/JS frontend)

## 5) Migration Notes

### Existing data shape risk
- Current persisted comments are strings in [app/storage.py](app/storage.py) and repository data file patterns.
- New feature requires comment objects, so old data must be interpreted safely.

### Planned migration approach
- On load, normalize comments:
  - if item is string, convert to structured object with generated id/task_id/created_at and body from string
  - author handling requires explicit decision (see Open Questions)
- Keep backward-read compatibility for existing task records that have no comments field or string comments.
- Write path should always persist structured comments once touched.
- Add migration-focused tests similar in spirit to existing legacy compatibility test style in [tests/test_tasks.py](tests/test_tasks.py).

### Important contract impact
- This is a response-shape change from comments as string[] to comments as object[].
- Frontend and tests must be updated together to avoid runtime/UI breakage.

## 6) Open Questions

1. Delete semantics
- Should delete remain index-based for backward compatibility, or move fully to comment-id-based endpoints?

2. Legacy comment author
- When migrating old string comments, what author value should be assigned (for example, Unknown), and is that acceptable for grading/product expectations?

3. Timestamp migration
- For migrated legacy comments, should created_at be:
  - migration time, or
  - task created_at, or
  - omitted (not preferred because model requires it)?

4. Response contract choice
- Should POST/DELETE comment routes continue returning full updated task (current pattern), or return only the created/deleted comment payload for smaller responses?

5. Ordering rule
- Should comments always be oldest-first, newest-first, or insertion order as currently implied?

6. Route transition strategy
- If comment-id delete is adopted, is a deprecation window required for index delete route used by current frontend?

## Files read
- [AGENTS.md](AGENTS.md)
- [README.md](README.md)
- [app/models.py](app/models.py)
- [app/main.py](app/main.py)
- [app/storage.py](app/storage.py)
- [app/business_rules.py](app/business_rules.py)
- [tests/test_tasks.py](tests/test_tasks.py)
- [tests/conftest.py](tests/conftest.py)
- [tests/verify_a.py](tests/verify_a.py)
- [frontend/index.html](frontend/index.html)

## Assumptions to verify
- Current course acceptance allows evolving comment shape from string list to object list.
- Returning full updated task from comment routes is still preferred for frontend simplicity.
- It is acceptable to add compatibility logic for legacy comments in storage loading.
- No additional route modules exist beyond [app/main.py](app/main.py) for this feature.
- No external auth/user identity system is required now; author remains free text.
