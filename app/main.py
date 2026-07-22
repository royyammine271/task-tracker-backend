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
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:8001",
        "http://127.0.0.1:8001",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/health", response_model=HealthResponse, status_code=200)
def health_check() -> HealthResponse:
    """
    Simple liveness check endpoint.

    Returns the current server status and an ISO-8601 UTC timestamp so
    clients (or monitoring tools) can confirm the API is up and see when
    the response was generated.
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
    return storage.add_task(payload)


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
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
    deleted = storage.delete_task(task_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return None


@app.post("/tasks/{task_id}/comments", response_model=TaskResponse, tags=["tasks"])
def add_task_comment(task_id: str, payload: TaskCommentCreate) -> TaskResponse:
    updated_task = storage.add_comment(task_id, payload.comment)

    if updated_task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    return updated_task