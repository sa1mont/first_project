from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str | None = Field(None, max_length=2000)
    priority: TaskPriority = TaskPriority.MEDIUM
    project_id: int

class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=150)
    description: str | None = Field(None, max_length=2000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assignee_id: int | None = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    project_id: int
    assignee_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}