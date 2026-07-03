from pydantic import BaseModel, Field
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str | None = None
    completed: bool = False
    completion_time: int | None = Field(default=None, ge=0)


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True