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

### Prompt Used

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

AI suggested keeping the feature small by adding one optional `due_date` field directly to each task. It recommended using Pydantic validation for the date format and computing overdue status using a simple rule: a task is overdue when its due date is before today and its status is not `Done`.

AI also suggested that backend-based overdue filtering would be easier to test with pytest and FastAPI TestClient, while the frontend could still show the due date and overdue pill visually.

### What I Accepted

I accepted:
- Adding `due_date` as an optional task field.
- Using `YYYY-MM-DD` as the accepted date format.
- Treating overdue as a simple computed condition.
- Computing overdue consistently in the backend for filtering.
- Showing the due date and overdue pill in the frontend.

### What I Edited

I kept the idea limited to due dates only, not due times. I also made sure the feature would work with the existing JSON file storage instead of introducing a database.

### What I Rejected

I rejected:
- Due times
- Recurring due dates
- Calendar integration
- Reminders or notifications
- User-specific deadlines
- Database migrations
- Large UI redesigns

These were too complex or out of scope for the learning project.

---

## Prompt 2: Implementation Prompt

### Prompt Used

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

AI returned implementation guidance for both backend and frontend changes. The backend changes included adding `due_date` to the Pydantic task models, saving it to JSON storage, supporting create and update behavior, and adding an optional overdue API filter.

The frontend changes included adding a date input to the task form or modal, displaying due dates on cards, showing an overdue pill, and adding an overdue filter control.

### What I Accepted

I accepted:
- Adding `due_date` to create, update, and response models.
- Saving `due_date` in the existing JSON task structure.
- Allowing `due_date` to be optional.
- Returning HTTP 422 for invalid date values.
- Adding `overdue=true` as an API filter.
- Showing a due date and overdue pill on the task cards.

### What I Edited

I checked that the AI implementation did not rename existing fields such as `title`, `description`, `status`, `priority`, or `assignee`.

I also kept the overdue rule simple and predictable: past due date plus status not equal to `Done`.

### What I Rejected

I rejected any implementation that introduced:
- New backend frameworks
- Database storage
- Time zone handling
- Due times
- Recurring dates
- Reminders
- Notifications
- Authentication
- A large frontend redesign

---

## Prompt 3: Testing Prompt

### Prompt Used

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

AI suggested a focused set of backend tests covering valid date creation, invalid date validation, optional due dates, updating due dates, overdue detection, and overdue filtering.

It also suggested regression tests to confirm that existing status and priority filters still worked after adding due date logic.

### What I Accepted

I accepted the API-level tests because they directly match the acceptance criteria and are easy to run with pytest.

### What I Edited

I planned to use clear fixed dates in the tests so the results would be easier to understand. For example, a past date should be used for overdue tasks and a future date should be used for non-overdue tasks.

### What I Rejected

I rejected tests for:
- Notifications
- Calendar behavior
- Time zones
- Due times
- Recurring due dates
- User-specific deadlines

Those behaviors are outside the selected feature scope.

---

# Feature 2: Task Comments

## Prompt 1: Idea Prompt

### Prompt Used

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

AI suggested keeping comments as a simple list stored directly inside each task. It recommended avoiding a separate comments table, users, timestamps, threaded comments, and editing or deleting comments.

AI also suggested adding a small endpoint for adding comments to a specific task and displaying comments inside the existing edit modal or task detail area.

### What I Accepted

I accepted:
- Storing comments directly with the task.
- Keeping comments simple as text values.
- Adding a comment section to the edit modal or task detail area.
- Showing comment count on task cards.
- Validating blank comments.

### What I Edited

I decided that comments should stay simple and should not include authors, timestamps, IDs, edit history, or delete behavior.

### What I Rejected

I rejected:
- Threaded comments
- Comment editing
- Comment deletion
- Authors or user attribution
- Timestamps
- Mentions
- Notifications
- Markdown formatting
- Real-time updates
- A separate comment database/table

These were too complex or out of scope.

---

## Prompt 2: Implementation Prompt

### Prompt Used

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

AI returned implementation guidance for adding comments to the backend task structure, creating a comment request model, adding a task-specific comment endpoint, validating blank comments, updating JSON persistence, and updating the frontend to display and submit comments.

### What I Accepted

I accepted:
- A `comments` field on each task.
- A simple endpoint such as `POST /tasks/{task_id}/comments`.
- Pydantic validation for non-blank comment text.
- HTTP 422 for blank comments.
- HTTP 404 for comments added to missing tasks.
- Returning the updated task after adding a comment.
- Showing comments and comment count in the frontend.

### What I Edited

I reviewed the suggested implementation to make sure existing tasks without a `comments` field would still load correctly by defaulting comments to an empty list.

I also kept the frontend simple by placing the comments section in the existing edit modal or task detail area instead of creating a new page.

### What I Rejected

I rejected implementation suggestions that added:
- Comment authors
- Timestamps
- Comment IDs
- Edit/delete functionality
- Threaded replies
- Markdown rendering
- Notifications
- Live updates
- A new database table
- A frontend framework

---

## Prompt 3: Testing Prompt

### Prompt Used

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

AI suggested API-level tests for adding comments, rejecting blank and whitespace-only comments, returning 404 for missing tasks, keeping comments attached to the correct task, and confirming older tasks without comments still load correctly.

### What I Accepted

I accepted the test cases because they directly verify the intended backend behavior and protect against common bugs.

### What I Edited

I adjusted the tests to match the actual response shape of the implemented API. If the endpoint returns the full updated task, the tests should check the `comments` list. If the frontend uses a count, the frontend verification should check the displayed count.

### What I Rejected

I rejected tests for:
- Comment editing
- Comment deletion
- Comment authors
- Timestamps
- Notifications
- Markdown formatting
- Live updates
- User permissions

Those behaviors were not part of the selected feature.

---

# Summary

The final prompt structure is intentionally simple:

- The first prompt defines the feature idea and limits the scope.
- The second prompt asks AI to actually implement the feature.
- The third prompt asks AI to add focused tests.

This format supports the required workflow: plan the feature, constrain it, implement it in small AI-assisted steps, inspect the output, verify behavior, test it, and document what happened.
