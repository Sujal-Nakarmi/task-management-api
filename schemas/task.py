
from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: str
    due_date: datetime

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()
    
    @field_validator('priority')
    def priority_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Priority cannot be empty')
        
        priority = v.strip().lower()
        allowed_priorities = ["high", "medium", "low"]

        if priority not in allowed_priorities:
            raise ValueError('Priority must be high, medium, or low')
        return priority

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

    @field_validator('priority')
    def priority_must_be_valid(cls, v):
        if v is None:
            return v
        
        if not v.strip():
            raise ValueError('Priority cannot be empty')

        priority = v.strip().lower()
        allowed_priorities = ["high", "medium", "low"]

        if priority not in allowed_priorities:
            raise ValueError('Priority must be high, medium, or low')
        return priority

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    priority: str
    due_date: datetime
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
