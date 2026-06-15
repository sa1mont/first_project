from datetime import datetime
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Название проекта")
    description: str | None = Field(None, max_length=1000, description="Описание проекта")

class ProjectOut(BaseModel):
    id: int
    title: str
    description: str | None
    creator_id: int
    created_at: datetime

    model_config = {"from_attributes": True}