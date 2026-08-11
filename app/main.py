"""
Entry point for the Task Tracker backend.

Creates the FastAPI application instance, loads configuration from a .env
file via python-dotenv, and exposes a GET /health endpoint used to verify
that the API process is running.
"""

import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.models import (
    TaskCommentCreate,
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskUpdate,
)
from app.schemas import HealthResponse

# Load environment variables from a .env file into the process environment.
# If no .env file is present, os.getenv() calls below simply fall back
# to their default values.
load_dotenv()

# Read basic config values. These aren't required for /health to work,
# but they demonstrate that env vars are wired up correctly.
APP_ENV = os.getenv("APP_ENV", "development")
PORT = int(os.getenv("PORT", "8000"))

# Create the FastAPI application instance.
app = FastAPI(
    title="Task Tracker API",
    description="Backend API for the Task Tracker learning project.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/health", response_model=HealthResponse, status_code=200)
def health_check() -> HealthResponse:
    """Return a lightweight liveness response.

    Args:
        None.

    Returns:
        HealthResponse: API status and a UTC ISO-8601 timestamp.

    Raises:
        None.

    Examples:
        GET /health
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task record.

    Args:
        payload (TaskCreate): Validated task creation input.

    Returns:
        TaskResponse: The created task with generated id and timestamps.

    Raises:
        None directly in this handler.

    Examples:
        POST /tasks
    """
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    """List tasks with optional status, priority, and overdue filters.

    Args:
        status (TaskStatus | None): Optional status filter.
        priority (TaskPriority | None): Optional priority filter.
        overdue (bool | None): Optional overdue filter.

    Returns:
        list[TaskResponse]: Tasks matching the provided filters.

    Raises:
        None directly in this handler.

    Examples:
        GET /tasks
        GET /tasks?status=InProgress
        GET /tasks?overdue=true
    """
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Get a single task by id.

    Args:
        task_id (str): Unique task identifier.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 when the task id is not found.

    Examples:
        GET /tasks/{task_id}
    """
    task = storage.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Apply a partial update to a task.

    Args:
        task_id (str): Unique task identifier.
        payload (TaskUpdate): Partial task fields to update.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: 404 when the task id is not found.
        HTTPException: 422 when status transition validation fails in storage rules.

    Examples:
        PATCH /tasks/{task_id}
    """
    updated_task = storage.update_task(task_id, payload)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> None:
    """Delete a task by id.

    Args:
        task_id (str): Unique task identifier.

    Returns:
        None: Empty response body with HTTP 204 on success.

    Raises:
        HTTPException: 404 when the task id is not found.

    Examples:
        DELETE /tasks/{task_id}
    """
    deleted = storage.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return None


@app.post("/tasks/{task_id}/comments", response_model=TaskResponse, tags=["tasks"])
def add_task_comment(task_id: str, payload: TaskCommentCreate) -> TaskResponse:
    """Append a comment to an existing task.

    Args:
        task_id (str): Unique task identifier.
        payload (TaskCommentCreate): Validated comment payload.

    Returns:
        TaskResponse: The updated task including appended comments.

    Raises:
        HTTPException: 404 when the task id is not found.

    Examples:
        POST /tasks/{task_id}/comments
    """
    updated_task = storage.add_comment(task_id, payload.comment)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return updated_task


@app.delete(
    "/tasks/{task_id}/comments/{comment_index}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def delete_task_comment(task_id: str, comment_index: int) -> TaskResponse:
    """Delete one comment from a task by index.

    Args:
        task_id (str): Unique task identifier.
        comment_index (int): Zero-based comment position to delete.

    Returns:
        TaskResponse: The updated task after comment removal.

    Raises:
        HTTPException: 404 when the task id is not found.
        HTTPException: 404 when the comment index does not exist for the task.

    Examples:
        DELETE /tasks/{task_id}/comments/{comment_index}
    """
    updated_task = storage.delete_comment(task_id, comment_index)

    if updated_task is None:
        task = storage.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        raise HTTPException(
            status_code=404,
            detail=f"Comment index {comment_index} not found for task {task_id}",
        )

    return updated_task