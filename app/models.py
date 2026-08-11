from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title must not be blank")
        if len(v) > 200:
            raise ValueError("title must be at most 200 characters")
        return v

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value):
        if value is None:
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("due_date must be a valid date in YYYY-MM-DD format")
        raise ValueError("due_date must be a valid date string")


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title must not be blank")
        if len(v) > 200:
            raise ValueError("title must be at most 200 characters")
        return v

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, value):
        if value is None:
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("due_date must be a valid date in YYYY-MM-DD format")
        raise ValueError("due_date must be a valid date string")


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    comments: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime


class TaskCommentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    comment: str

    @field_validator("comment")
    @classmethod
    def validate_comment(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("comment must not be blank")
        return v
