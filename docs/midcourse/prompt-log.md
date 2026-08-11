# AI Prompt Log for Module 1 Task Tracker Feature Pack

## Purpose

This document records the AI-assisted workflow prompts used for the two selected Module 1 Task Tracker features:

1. Due dates + overdue filter
2. Task comments

The prompt log is organized into exactly three prompts per feature:

1. Idea prompt
2. Implementation prompt
3. Testing prompt

Each prompt includes:
- The prompt used
- What AI returned
- What I accepted, edited, or rejected

---

# Feature 1: Due Dates + Overdue Filter

## Prompt 1: Idea Prompt

### Weak Prompt

```text
Help me with due dates.
```

### Strong Prompt Used

```text
Before writing code, help me define the idea for this feature clearly.

Feature: Due dates + overdue filter

Current project:
I am building a simple Task Tracker using FastAPI, Pydantic, JSON file storage, and a separate vanilla HTML/CSS/JavaScript frontend.

Expected backend idea:
- Add an optional due_date field to tasks.
- Validate due_date using Pydantic.
- Decide whether overdue should be calculated in the backend or frontend.
- Optionally support an overdue filter in the API.

Expected frontend idea:
- Add due date to the create/edit modal or form.
- Show due date on task cards.
- Show an overdue pill or visual indicator.
- Add an overdue filter control.

Constraints:
- Do not write code yet.
- Keep the feature small and aligned with the current architecture.
- Do not add authentication, notifications, recurring dates, due times, Docker, a database, or a frontend framework.
- Explain the simplest design choice and what should stay out of scope.
```

### What AI Returned

AI recommended adding one optional due_date field, validating date format with Pydantic, and using a simple overdue rule: due date before today and status not Done. It also recommended backend overdue filtering for easier testability.

### What I Accepted

- Optional due_date field.
- YYYY-MM-DD date format.
- Simple overdue rule.
- Backend-based overdue filtering.
- Due date and overdue pill in the frontend.

### What I Edited

- Limited scope to due dates only (no due times).
- Kept JSON storage and existing architecture.

### What I Rejected

- Recurring dates, reminders, calendar integration, notifications, and large UI redesign.

## Feature 1, Prompt 2: Implementation Prompt

### Weak Prompt

```text
Implement due dates and overdue filter.
```

### Strong Prompt Used

```text
Implement the Feature 1 changes in small, focused edits.

Feature: Due dates + overdue filter

Backend requirements:
- Add an optional due_date field to the task create, update, and response models.
- due_date should accept only valid dates in YYYY-MM-DD format using Pydantic validation.
- Invalid due_date values should return HTTP 422.
- due_date must be saved to and loaded from the existing JSON file storage.
- Updating a task should support changing due_date or removing due_date.
- Add overdue behavior:
  - A task is overdue when due_date is before today's date and status is not Done.
  - Done tasks are not overdue even if the due_date is in the past.
  - Tasks without due_date are not overdue.
- Add an optional API filter for overdue tasks, such as overdue=true.
- Keep the existing status and priority filters working.

Frontend requirements:
- Add a due date input to the existing create/edit modal or form.
- Show the due date on task cards when it exists.
- Show an overdue pill or visual indicator on overdue task cards.
- Add an overdue filter control.
- Keep the current frontend structure and do not redesign the whole UI.

Constraints:
- Use the existing FastAPI, Pydantic, JSON storage, and vanilla JS structure.
- Do not add a database, authentication, notifications, recurring dates, due times, Docker, or a frontend framework.
- Do not modify unrelated features.
- After making the code changes, summarize exactly which files changed and why.
```

### What AI Returned

AI provided backend and frontend implementation guidance: model updates, validation, persistence, overdue filter, modal input, card display, and overdue control.

### What I Accepted

- due_date in create/update/response.
- 422 validation for invalid dates.
- JSON persistence updates.
- overdue=true API filter.
- due date and overdue pill UI.

### What I Edited

- Verified no renaming of existing task fields.
- Kept overdue logic minimal and predictable.

### What I Rejected

- Database/storage redesign, timezone complexity, due times, recurring features, and broad UI redesign.

## Feature 1, Prompt 3: Testing Prompt

### Weak Prompt

```text
Write tests for due dates.
```

### Strong Prompt Used

```text
Add focused pytest + FastAPI TestClient tests for the due dates + overdue filter feature.

Test requirements:
- Creating a task with a valid due_date succeeds.
- Creating a task with an invalid due_date returns HTTP 422.
- Creating a task without due_date still succeeds.
- Updating a task due_date succeeds.
- Removing a task due_date succeeds if supported by the update model.
- A task with a past due_date and status not Done is treated as overdue.
- A task with status Done is not treated as overdue, even when the due_date is in the past.
- A task without due_date is not treated as overdue.
- The overdue=true filter returns only overdue tasks.
- Existing status and priority filters still work after the due date changes.

Constraints:
- Use the existing pytest style and fixtures.
- Use FastAPI TestClient.
- Do not introduce a database or external service.
- Keep each test small and readable.
- Do not change production code unless the tests reveal a real defect.
```

### What AI Returned

AI suggested a focused test set for valid/invalid due dates, optional due date behavior, overdue logic, and filter/regression coverage.

### What I Accepted

- API-level tests aligned to acceptance criteria.

### What I Edited

- Planned clear date choices (past vs future) for readable test intent.

### What I Rejected

- Tests for notifications, time zones, due times, recurring dates, and user-specific deadline behavior.

# Feature 2: Task comments

## Prompt 1: Idea Prompt

### Weak Prompt

```text
Help me add task comments.
```

### Strong Prompt Used

```text
Before writing code, help me define the idea for this feature clearly.

Feature: Task comments

Current project:
I am building a simple Task Tracker using FastAPI, Pydantic, JSON file storage, and a separate vanilla HTML/CSS/JavaScript frontend.

Expected backend idea:
- Add a comments field to tasks.
- Support adding a comment to an existing task.
- Validate that comments are not blank.
- Return 404 if the task does not exist.

Expected frontend idea:
- Add a comments section in the edit modal or a small task detail area.
- Show existing comments.
- Allow adding a new comment.
- Show comment count on task cards.

Constraints:
- Do not write code yet.
- Keep the feature small.
- Keep JSON file storage.
- Do not add users, authors, timestamps, notifications, real-time updates, comment editing, comment deletion, markdown support, or a frontend framework.
- Explain the simplest design choice and what should stay out of scope.
```

### What AI Returned

AI recommended storing comments as a simple list on each task and adding a lightweight task-specific comment endpoint and modal UI.

### What I Accepted

- Comments stored on the task.
- Simple text comments.
- Comments section in edit modal/detail area.
- Comment count on cards.
- Blank comment validation.

### What I Edited

- Kept comments minimal without metadata fields.

### What I Rejected

- Threading, authors, timestamps, mentions, markdown, real-time updates, and separate comments table.

## Feature 2, Prompt 2: Implementation Prompt

### Weak Prompt

```text
Implement comments.
```

### Strong Prompt Used

```text
Implement the Feature 2 changes in small, focused edits.

Feature: Task comments

Backend requirements:
- Store comments with the correct task using the existing JSON file storage.
- Add a comments field to each task. Keep it simple as a list of strings unless the current code structure requires a small object.
- Existing tasks without comments should still load correctly by defaulting comments to an empty list.
- Add a Pydantic request model for adding a comment.
- The comment text is required and cannot be blank or whitespace-only.
- Blank comments should return HTTP 422.
- Add a REST endpoint such as POST /tasks/{task_id}/comments.
- Adding a comment to a missing task should return HTTP 404.
- Return the updated task after a comment is added so the frontend can refresh the card and comment count.

Frontend requirements:
- Add a comments section to the existing edit modal or task detail area.
- Show existing comments for the selected task.
- Add a textarea or input for a new comment.
- Add a button to submit the new comment.
- Show the comment count on each task card.
- After a comment is added, update the comments section and task card count.
- Show an error message if the comment is blank or the backend request fails.

Constraints:
- Use the existing FastAPI, Pydantic, JSON storage, and vanilla JS structure.
- Do not add users, authors, timestamps, notifications, markdown formatting, comment editing, comment deletion, a database, Docker, or a frontend framework.
- Do not modify unrelated features.
- After making the code changes, summarize exactly which files changed and why.
```

### What AI Returned

AI returned guidance for backend model/storage/endpoint changes and frontend modal/comment-count updates.

### What I Accepted

- comments field.
- POST /tasks/{task_id}/comments endpoint.
- Non-blank validation with 422.
- Missing task 404.
- Updated task response shape.
- Frontend comment list + count.

### What I Edited

- Verified legacy tasks default comments to [].
- Kept UI in existing modal rather than new page.

### What I Rejected

- Metadata-heavy comments, threaded replies, markdown rendering, notifications, and framework/database additions.

## Feature 2, Prompt 3: Testing Prompt

### Weak Prompt

```text
Add tests for comments.
```

### Strong Prompt Used

```text
Add focused pytest + FastAPI TestClient tests for the task comments feature.

Test requirements:
- Adding a comment to an existing task succeeds.
- The response includes the new comment.
- Blank comments return HTTP 422.
- Whitespace-only comments return HTTP 422.
- Adding a comment to a missing task returns HTTP 404.
- Comments stay attached to the correct task.
- Existing tasks without comments default to an empty comments list.
- The returned task includes an accurate comments list or comment count, depending on the implemented response shape.

Constraints:
- Use the existing pytest style and fixtures.
- Use FastAPI TestClient.
- Do not introduce a database or external service.
- Keep each test small and readable.
- Do not test users, authors, timestamps, editing, deleting, notifications, or real-time updates.
- Do not change production code unless the tests reveal a real defect.
```

### What AI Returned

AI suggested tests for successful add flow, validation failures, missing-task failures, task attachment integrity, and legacy comments defaults.

### What I Accepted

- Core API tests directly tied to acceptance criteria.

### What I Edited

- Matched assertions to actual endpoint response shape (comments list vs displayed count).

### What I Rejected

- Tests for out-of-scope features such as authors, timestamps, notifications, live updates, and permissions.