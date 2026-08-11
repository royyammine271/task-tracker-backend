import json
import os
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_DATA_FILE = os.getenv("TASKS_DATA_FILE", str(Path(__file__).resolve().parent / "tasks.json"))
_tasks: dict[str, TaskResponse] = {}


def _load_tasks() -> None:
    global _tasks
    if not os.path.exists(_DATA_FILE):
        _tasks = {}
        return

    with open(_DATA_FILE, "r", encoding="utf-8") as handle:
        raw_tasks = json.load(handle)

    _tasks = {
        task_id: TaskResponse(**task_data)
        for task_id, task_data in raw_tasks.items()
    }


def _save_tasks() -> None:
    with open(_DATA_FILE, "w", encoding="utf-8") as handle:
        json.dump(
            {task_id: task.model_dump() for task_id, task in _tasks.items()},
            handle,
            indent=2,
            default=str,
        )


_load_tasks()


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and persist a new task.

    Args:
        payload (TaskCreate): Validated task creation payload.

    Returns:
        TaskResponse: Newly created persisted task.

    Raises:
        OSError: If writing the JSON data file fails.
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        comments=[],
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    _save_tasks()
    return task


def _is_overdue(task: TaskResponse) -> bool:
    if task.status == TaskStatus.DONE:
        return False
    if task.due_date is None:
        return False
    return task.due_date < date.today()


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    """Return all tasks filtered by optional criteria.

    Args:
        status (Optional[TaskStatus]): Optional status filter.
        priority (Optional[TaskPriority]): Optional priority filter.
        overdue (Optional[bool]): Optional overdue-state filter.

    Returns:
        list[TaskResponse]: Tasks that match all provided filters.

    Raises:
        json.JSONDecodeError: If persisted task data is malformed.
    """
    _load_tasks()
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    if overdue is not None:
        tasks = [t for t in tasks if _is_overdue(t) is overdue]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Get one task by id.

    Args:
        task_id (str): Unique task identifier.

    Returns:
        Optional[TaskResponse]: Matching task if found, otherwise None.

    Raises:
        json.JSONDecodeError: If persisted task data is malformed.
    """
    _load_tasks()
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Update an existing task and persist changes.

    Args:
        task_id (str): Unique task identifier.
        payload (TaskUpdate): Partial update payload.

    Returns:
        Optional[TaskResponse]: Updated task, unchanged task when no fields are
            provided, or None when task does not exist.

    Raises:
        HTTPException: 422 when status transition validation fails.
        OSError: If writing the JSON data file fails.
    """
    _load_tasks()
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    if "status" in updates:
        validate_status_transition(task.status, updates["status"])

    now = datetime.now(timezone.utc)
    updated_data = task.model_dump()
    updated_data.update(updates)
    updated_data["updated_at"] = now

    updated_task = TaskResponse(**updated_data)
    _tasks[task_id] = updated_task
    _save_tasks()
    return updated_task


def delete_task(task_id: str) -> bool:
    """Delete a task by id.

    Args:
        task_id (str): Unique task identifier.

    Returns:
        bool: True when a task was deleted, False when it was not found.

    Raises:
        OSError: If writing the JSON data file fails after deletion.
    """
    _load_tasks()
    if task_id in _tasks:
        del _tasks[task_id]
        _save_tasks()
        return True
    return False


def add_comment(task_id: str, comment: str) -> Optional[TaskResponse]:
    """Append a comment to a task and persist changes.

    Args:
        task_id (str): Unique task identifier.
        comment (str): Comment text already validated by request model.

    Returns:
        Optional[TaskResponse]: Updated task when found, otherwise None.

    Raises:
        OSError: If writing the JSON data file fails.
    """
    _load_tasks()
    task = _tasks.get(task_id)
    if task is None:
        return None

    now = datetime.now(timezone.utc)
    updated_data = task.model_dump()
    updated_data["comments"] = [*task.comments, comment]
    updated_data["updated_at"] = now

    updated_task = TaskResponse(**updated_data)
    _tasks[task_id] = updated_task
    _save_tasks()
    return updated_task


def delete_comment(task_id: str, comment_index: int) -> Optional[TaskResponse]:
    """Delete a task comment by zero-based index.

    Args:
        task_id (str): Unique task identifier.
        comment_index (int): Zero-based index of the comment to remove.

    Returns:
        Optional[TaskResponse]: Updated task when task and index exist,
            otherwise None.

    Raises:
        OSError: If writing the JSON data file fails.
    """
    _load_tasks()
    task = _tasks.get(task_id)
    if task is None:
        return None

    if comment_index < 0 or comment_index >= len(task.comments):
        return None

    now = datetime.now(timezone.utc)
    updated_data = task.model_dump()
    updated_comments = list(task.comments)
    del updated_comments[comment_index]
    updated_data["comments"] = updated_comments
    updated_data["updated_at"] = now

    updated_task = TaskResponse(**updated_data)
    _tasks[task_id] = updated_task
    _save_tasks()
    return updated_task


def _reset() -> None:
    _tasks.clear()
    _save_tasks()
