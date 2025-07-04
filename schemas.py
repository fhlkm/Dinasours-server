from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    userId: int = Field(..., ge=1, description="User ID must be a positive integer")
    taskName: str = Field(..., min_length=1, max_length=200, description="Task name cannot be empty")
    category: str = Field(..., min_length=1, max_length=100, description="Category cannot be empty")
    time: str = Field(..., description="Time in ISO format or human-readable format")
    status: str = Field(..., min_length=1, max_length=50, description="Status cannot be empty")
    
    @validator('taskName')
    def validate_task_name(cls, v):
        if not v.strip():
            raise ValueError('Task name cannot be empty or whitespace only')
        return v.strip()
    
    @validator('category')
    def validate_category(cls, v):
        if not v.strip():
            raise ValueError('Category cannot be empty or whitespace only')
        return v.strip()
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled', 'on_hold']
        if v.lower() not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v.lower()
    
    class Config:
        schema_extra = {
            "example": {
                "userId": 1,
                "taskName": "Complete project documentation",
                "category": "work",
                "time": "2025-07-04T10:00:00",
                "status": "pending"
            }
        }

class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    taskId: int = Field(..., ge=1, description="Task ID must be a positive integer")
    userId: int = Field(..., ge=1, description="User ID must be a positive integer")
    taskName: str = Field(..., min_length=1, max_length=200, description="Task name cannot be empty")
    category: str = Field(..., min_length=1, max_length=100, description="Category cannot be empty")
    time: str = Field(..., description="Time in ISO format or human-readable format")
    status: str = Field(..., min_length=1, max_length=50, description="Status cannot be empty")
    
    @validator('taskName')
    def validate_task_name(cls, v):
        if not v.strip():
            raise ValueError('Task name cannot be empty or whitespace only')
        return v.strip()
    
    @validator('category')
    def validate_category(cls, v):
        if not v.strip():
            raise ValueError('Category cannot be empty or whitespace only')
        return v.strip()
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled', 'on_hold']
        if v.lower() not in valid_statuses:
            raise ValueError(f'Status must be one of: {", ".join(valid_statuses)}')
        return v.lower()
    
    class Config:
        schema_extra = {
            "example": {
                "taskId": 1,
                "userId": 1,
                "taskName": "Complete project documentation - Updated",
                "category": "work",
                "time": "2025-07-04T12:00:00",
                "status": "in_progress"
            }
        }

class TaskResponse(BaseModel):
    """Schema for task response"""
    taskId: int
    userId: int
    taskName: str
    category: str
    time: str
    status: str
    
    class Config:
        schema_extra = {
            "example": {
                "taskId": 1,
                "userId": 1,
                "taskName": "Complete project documentation",
                "category": "work",
                "time": "2025-07-04T10:00:00",
                "status": "pending"
            }
        }

class TaskDelete(BaseModel):
    """Schema for task deletion response"""
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Task with ID 1 deleted successfully"
            }
        }

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    
    class Config:
        schema_extra = {
            "example": {
                "detail": "Task with ID 1 not found"
            }
        }

class TaskStats(BaseModel):
    """Schema for task statistics"""
    total_tasks: int
    pending_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    
    class Config:
        schema_extra = {
            "example": {
                "total_tasks": 10,
                "pending_tasks": 3,
                "completed_tasks": 5,
                "in_progress_tasks": 2
            }
        }
