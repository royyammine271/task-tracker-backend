# User Stories for Module 1 Task Tracker

## Selected Features

This document records the two selected features for the Module 1 Task Tracker project and the corrected user stories drafted with AI support.

Selected features:

1. Due dates + overdue filter
2. Task comments

## Review and Corrected Assumptions

The initial AI-generated stories needed correction because some stories repeated the original Module 1 CRUD functionality instead of focusing on the selected new features.

For Feature 1, the stories should focus only on due dates, overdue indicators, due date validation, updates, and overdue filtering.

For Feature 2, the stories should focus only on task comments, comment validation, displaying comments, and comment counts.

The corrected stories below keep the role as **team member**, avoid out-of-scope items such as authentication or notifications, and include clear success and failure cases.

---

# Feature 1: Due Dates + Overdue Filter

## Story 1

**Story:** As a team member, I want to add an optional due date when creating a task so that I can track when work should be completed.

**Acceptance Criteria:**

- Due date is optional when creating a task.
- If a valid due date is provided, the created task stores the due date.
- The created task appears in the task list with its title, status, priority, assignee, and due date.
- If an invalid due date format is submitted, the API returns HTTP 422 and the task is not created.

---

## Story 2

**Story:** As a team member, I want to update a task's due date so that I can keep the deadline accurate when plans change.

**Acceptance Criteria:**

- Updating an existing task with a valid due date saves and displays the new due date.
- Updating a task to remove the due date saves the task with no due date.
- Updating a task with an invalid due date format returns HTTP 422.
- Updating the due date of a task that does not exist returns HTTP 404.

---

## Story 3

**Story:** As a team member, I want overdue tasks to show a clear overdue indicator so that I can quickly identify work that needs attention.

**Acceptance Criteria:**

- A task with a due date before today and a status other than `Done` is marked as overdue.
- A task with status `Done` is not marked as overdue, even if its due date has passed.
- A task without a due date is not marked as overdue.
- Overdue tasks display a clear visual label or pill on the task card.

---

## Story 4

**Story:** As a team member, I want to filter the task list to show only overdue tasks so that I can focus on late work first.

**Acceptance Criteria:**

- When the overdue filter is selected, only overdue tasks are shown.
- When the overdue filter is cleared, the task list returns to the normal filtered view.
- If no overdue tasks exist, the frontend shows a clear empty-state message.
- If an invalid overdue filter value is sent to the API, the API returns a validation error.

---

## Story 5

**Story:** As a team member, I want due dates to stay visible on task cards so that I can understand deadlines without opening each task.

**Acceptance Criteria:**

- A task with a due date displays the due date on its card.
- A task without a due date does not display an incorrect or placeholder deadline.
- Updating a task's due date updates the due date shown on the card.
- If the task list fails to load, the frontend shows an error message instead of a broken card layout.

---

# Feature 2: Task Comments

## Story 1

**Story:** As a team member, I want to add a comment to an existing task so that I can record notes or progress updates about the work.

**Acceptance Criteria:**

- A comment can be added to an existing task.
- A comment cannot be blank; submitting an empty or whitespace-only comment returns HTTP 422.
- Added comments are saved with the task.
- Adding a comment to a task that does not exist returns HTTP 404.

---

## Story 2

**Story:** As a team member, I want to view comments inside the task edit modal or task detail area so that I can understand previous notes before making changes.

**Acceptance Criteria:**

- Existing comments are displayed when the task detail area or edit modal is opened.
- Comments are shown in the order they were added.
- A task with no comments shows a clear empty-state message such as “No comments yet.”
- If comments fail to load, the frontend shows an error message instead of a broken detail area.

---

## Story 3

**Story:** As a team member, I want to see the comment count on each task card so that I can quickly identify which tasks have extra notes.

**Acceptance Criteria:**

- A task card shows the correct comment count when comments exist.
- A task with no comments shows either no count or a count of `0`, depending on the chosen UI design.
- The comment count updates after a new comment is added.
- The comment count remains accurate after refreshing the task list.

---

## Story 4

**Story:** As a team member, I want task comments to be stored with the correct task so that notes do not appear under the wrong work item.

**Acceptance Criteria:**

- A comment added to one task appears only under that task.
- A comment added to one task does not change the comments of another task.
- Refreshing the page keeps comments associated with the correct task.
- If the backend cannot find the task, the API returns HTTP 404 and does not save the comment.

---

## Story 5

**Story:** As a team member, I want the comments section to be simple and visible in the task workflow so that I can add notes without leaving the task tracker page.

**Acceptance Criteria:**

- The comments section is available from the edit modal or a small task detail area.
- A new comment can be submitted from the same page as the task list.
- After a comment is added, the comments section shows the new comment without requiring manual data entry again.
- If the comment request fails, the frontend shows an error message and does not display the comment as successfully saved.

---

# AI Support Reflection

AI was used to draft initial user stories for the two selected features. The first AI output included general CRUD stories that were already part of the base Module 1 Task Tracker scope, so those stories were corrected to focus specifically on the new due date and overdue filter feature.

The second AI output mixed due date stories with comment stories, even though it was meant to focus on task comments. This assumption was corrected by separating the selected features clearly and rewriting the stories so each feature has its own focused set of acceptance criteria.

The final stories are intentionally small, testable, and suitable for a solo developer learning FastAPI, Pydantic validation, frontend integration, and pytest-based testing.
