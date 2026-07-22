import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

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
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    _save_tasks()
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    _load_tasks()
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    _load_tasks()
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    _load_tasks()
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    now = datetime.now(timezone.utc)
    updated_data = task.model_dump()
    updated_data.update(updates)
    updated_data["updated_at"] = now

    updated_task = TaskResponse(**updated_data)
    _tasks[task_id] = updated_task
    _save_tasks()
    return updated_task


def delete_task(task_id: str) -> bool:
    _load_tasks()
    if task_id in _tasks:
        del _tasks[task_id]
        _save_tasks()
        return True
    return False


def _reset() -> None:
    _tasks.clear()
    _save_tasks()
