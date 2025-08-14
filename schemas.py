from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
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
        json_schema_extra = {
            "example": {
                "taskName": "Complete project documentation",
                "category": "work",
                "time": "2025-07-04T10:00:00",
                "status": "pending"
            }
        }

class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    taskId: int = Field(..., ge=1, description="Task ID must be a positive long integer")
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
        json_schema_extra = {
            "example": {
                "taskId": 1,
                "taskName": "Complete project documentation - Updated",
                "category": "work",
                "time": "2025-07-04T12:00:00",
                "status": "in_progress"
            }
        }

class TaskResponse(BaseModel):
    """Schema for task response"""
    taskId: int  # Will be Long in JSON
    userId: str  # Changed from int to str to match UUID strings used for user IDs
    taskName: str
    category: str
    time: str
    status: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "taskId": 1,
                "userId": "80975f27-ce40-4d72-b448-68516f",
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
        json_schema_extra = {
            "example": {
                "message": "Task with ID 1 deleted successfully"
            }
        }

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    
    class Config:
        json_schema_extra = {
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
        json_schema_extra = {
            "example": {
                "total_tasks": 10,
                "pending_tasks": 3,
                "completed_tasks": 5,
                "in_progress_tasks": 2
            }
        }

class PaginatedTaskResponse(BaseModel):
    """Schema for paginated task response"""
    tasks: List[TaskResponse]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "taskId": 1,
                        "userId": 1,
                        "taskName": "Complete project documentation",
                        "category": "work",
                        "time": "2025-07-04T10:00:00",
                        "status": "pending"
                    }
                ],
                "total_count": 50,
                "page": 1,
                "page_size": 20,
                "total_pages": 3,
                "has_next": True,
                "has_previous": False
            }
        }

class UserRegister(BaseModel):
    """Schema for user registration"""
    email: str = Field(..., description="User's email address")
    relationship: str = Field(..., min_length=1, max_length=50, description="User's relationship")
    password: str = Field(..., min_length=6, max_length=100, description="User's password (min 6 characters)")
    gender: str = Field(..., min_length=1, max_length=20, description="User's gender")
    nickname: str = Field(..., min_length=1, max_length=50, description="User's nickname")
    birthday: str = Field(..., description="User's birthday in ISO format")
    
    @validator('email')
    def validate_email(cls, v):
        if not v.strip():
            raise ValueError('Email cannot be empty or whitespace only')
        if '@' not in v:
            raise ValueError('Email must contain @ symbol')
        return v.strip().lower()
    
    @validator('relationship')
    def validate_relationship(cls, v):
        if not v.strip():
            raise ValueError('Relationship cannot be empty or whitespace only')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v.strip():
            raise ValueError('Password cannot be empty or whitespace only')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v.strip()
    
    @validator('gender')
    def validate_gender(cls, v):
        if not v.strip():
            raise ValueError('Gender cannot be empty or whitespace only')
        return v.strip()
    
    @validator('nickname')
    def validate_nickname(cls, v):
        if not v.strip():
            raise ValueError('Nickname cannot be empty or whitespace only')
        return v.strip()
    
    @validator('birthday')
    def validate_birthday(cls, v):
        if not v.strip():
            raise ValueError('Birthday cannot be empty or whitespace only')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "relationship": "friend",
                "password": "securepassword123",
                "gender": "male",
                "nickname": "John",
                "birthday": "1990-01-01"
            }
        }

class UserRegisterResponse(BaseModel):
    """Schema for user registration response"""
    userId: str
    email: str
    relationship: str
    gender: str
    nickname: str
    birthday: str
    message: str
    session: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "userId": "abc123-def456-ghi789",
                "email": "john.doe@example.com",
                "relationship": "friend",
                "gender": "male",
                "nickname": "John",
                "birthday": "1990-01-01",
                "message": "User registered successfully",
                "session": {
                    "sessionToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWJjMTIzLWRlZjQ1Ni1naGk3ODkiLCJzZXNzaW9uX2lkIjoiMTIzNDU2Nzg5MCIsImV4cCI6MTczNTY3ODkwMH0.signature_part_here",
                    "expiresAt": "2025-08-03T15:30:00Z"
                }
            }
        }

class UserLogin(BaseModel):
    """Schema for user login"""
    email: str = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")
    
    @validator('email')
    def validate_email(cls, v):
        if not v.strip():
            raise ValueError('Email cannot be empty or whitespace only')
        return v.strip().lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not v.strip():
            raise ValueError('Password cannot be empty or whitespace only')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "securepassword123"
            }
        }

class UserLoginResponse(BaseModel):
    """Schema for user login response"""
    userId: str
    email: str
    relationship: str
    gender: str
    nickname: str
    birthday: str
    message: str
    session: dict
    
    class Config:
        json_schema_extra = {
            "example": {
                "userId": "abc123-def456-ghi789",
                "email": "john.doe@example.com",
                "relationship": "friend",
                "gender": "male",
                "nickname": "John",
                "birthday": "1990-01-01",
                "message": "Login successful",
                "session": {
                    "sessionToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWJjMTIzLWRlZjQ1Ni1naGk3ODkiLCJzZXNzaW9uX2lkIjoiMTIzNDU2Nzg5MCIsImV4cCI6MTczNTY3ODkwMH0.signature_part_here",
                    "expiresAt": "2025-08-03T15:30:00Z"
                }
            }
        }

class CompletedTasksByCategoryResponse(BaseModel):
    """Schema for completed tasks by category response"""
    category: str
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "work",
                "count": 5
            }
        }
