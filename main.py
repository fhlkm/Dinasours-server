from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
from database import get_db, init_db, get_db_context
from models import TaskModel
from schemas import TaskCreate, TaskUpdate, TaskResponse, UserRegister, UserRegisterResponse, UserLogin, UserLoginResponse
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for database initialization"""
    try:
        init_db()
        logger.info("Database initialized successfully")
        
        # Cleanup expired sessions on startup
        with get_db_context() as db:
            task_model = TaskModel(db)
            deleted_count = task_model.cleanup_expired_sessions()
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired sessions on startup")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    yield

app = FastAPI(
    title="Task Management API",
    description="A FastAPI-based task management system with SQLite database",
    version="1.0.0",
    lifespan=lifespan
)

# Session validation dependency
async def get_current_user(authorization: str = Header(None), db=Depends(get_db)) -> str:
    """Validate session and return user ID"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Valid session token is required")
    
    session_token = authorization.replace("Bearer ", "")
    
    try:
        task_model = TaskModel(db)
        user_id = task_model.validate_session(session_token)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Session expired or invalid")
        
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to validate session")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "endpoints": {
            "create_task": "POST /task",
            "update_task": "PUT /task",
            "delete_task": "DELETE /task/{task_id}",
            "get_all_tasks": "GET /tasks",
            "get_user_tasks": "GET /tasks/user/{user_id}"
        }
    }

@app.post("/task", response_model=TaskResponse)
async def create_task(
    task: TaskCreate, 
    current_user_id: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Create a new task"""
    try:
        task_model = TaskModel(db)
        task_id = task_model.create_task(
            user_id=current_user_id,  # Use validated user ID from session
            task_name=task.taskName,
            category=task.category,
            time=task.time,
            status=task.status
        )
        
        # Retrieve the created task
        created_task = task_model.get_task_by_id(task_id)
        if not created_task:
            raise HTTPException(status_code=500, detail="Failed to retrieve created task")
        
        logger.info(f"Task created successfully with ID: {task_id} for user: {current_user_id}")
        return TaskResponse(
            taskId=created_task[0],
            userId=created_task[1],
            taskName=created_task[2],
            category=created_task[3],
            time=created_task[4],
            status=created_task[5]
        )
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")

@app.put("/task", response_model=TaskResponse)
async def update_task(
    task: TaskUpdate, 
    current_user_id: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Update an existing task"""
    try:
        task_model = TaskModel(db)
        
        # Check if task exists and belongs to current user
        existing_task = task_model.get_task_by_id(task.taskId)
        if not existing_task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task.taskId} not found")
        
        # Verify task ownership
        if existing_task[1] != current_user_id:
            raise HTTPException(status_code=403, detail="You can only update your own tasks")
        
        # Update task
        success = task_model.update_task(
            task_id=task.taskId,
            user_id=current_user_id,  # Use validated user ID from session
            task_name=task.taskName,
            category=task.category,
            time=task.time,
            status=task.status
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update task")
        
        # Retrieve updated task
        updated_task = task_model.get_task_by_id(task.taskId)
        logger.info(f"Task updated successfully with ID: {task.taskId} for user: {current_user_id}")
        
        return TaskResponse(
            taskId=updated_task[0],
            userId=updated_task[1],
            taskName=updated_task[2],
            category=updated_task[3],
            time=updated_task[4],
            status=updated_task[5]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")

@app.delete("/task/{task_id}")
async def delete_task(
    task_id: int, 
    current_user_id: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Delete a task by ID"""
    try:
        task_model = TaskModel(db)
        
        # Check if task exists and belongs to current user
        existing_task = task_model.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
        # Verify task ownership
        if existing_task[1] != current_user_id:
            raise HTTPException(status_code=403, detail="You can only delete your own tasks")
        
        # Delete task
        success = task_model.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete task")
        
        logger.info(f"Task deleted successfully with ID: {task_id} by user: {current_user_id}")
        return {"message": f"Task with ID {task_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

@app.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks(
    current_user_id: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get all tasks sorted by time in descending order"""
    try:
        task_model = TaskModel(db)
        tasks = task_model.get_all_tasks()
        
        task_list = []
        for task in tasks:
            task_list.append(TaskResponse(
                taskId=task[0],
                userId=task[1],
                taskName=task[2],
                category=task[3],
                time=task[4],
                status=task[5]
            ))
        
        logger.info(f"Retrieved {len(task_list)} tasks for user: {current_user_id}")
        return task_list
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")

@app.get("/tasks/user/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks(
    user_id: str, 
    current_user_id: str = Depends(get_current_user),
    db=Depends(get_db)
):
    """Get all tasks for a specific user sorted by time in descending order"""
    try:
        # Ensure users can only access their own tasks
        if user_id != current_user_id:
            raise HTTPException(status_code=403, detail="You can only access your own tasks")
        
        task_model = TaskModel(db)
        tasks = task_model.get_tasks_by_user(user_id)
        
        task_list = []
        for task in tasks:
            task_list.append(TaskResponse(
                taskId=task[0],
                userId=task[1],
                taskName=task[2],
                category=task[3],
                time=task[4],
                status=task[5]
            ))
        
        logger.info(f"Retrieved {len(task_list)} tasks for user {user_id}")
        return task_list
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks for user: {str(e)}")

@app.post("/register", response_model=UserRegisterResponse, status_code=201)
async def register_user(user: UserRegister, db=Depends(get_db)):
    """Register a new user"""
    try:
        task_model = TaskModel(db)
        user_id = task_model.add_new_member(
            email=user.email,
            relationship=user.relationship,
            password=user.password,
            gender=user.gender,
            nickname=user.nickname,
            birth=user.birthday
        )
        
        # Create new session for the user after successful registration
        session_info = task_model.create_session(user_id)
        
        logger.info(f"User registered successfully with ID: {user_id}")
        return UserRegisterResponse(
            userId=user_id,
            message="User registered successfully",
            session=session_info
        )
    except Exception as e:
        error_message = str(e)
        if "email might already exist" in error_message:
            logger.warning(f"Registration failed - email already exists: {user.email}")
            raise HTTPException(status_code=409, detail="Email already exists")
        else:
            logger.error(f"Error registering user: {error_message}")
            raise HTTPException(status_code=500, detail=f"Failed to register user: {error_message}")

@app.post("/login", response_model=UserLoginResponse)
async def login_user(user: UserLogin, db=Depends(get_db)):
    """Login user with email and password"""
    try:
        task_model = TaskModel(db)
        user_id = task_model.getUser(
            email=user.email,
            password=user.password
        )
        
        if user_id:
            # Create new session for the user
            session_info = task_model.create_session(user_id)
            
            logger.info(f"User logged in successfully: {user_id}")
            return UserLoginResponse(
                userId=user_id,
                message="Login successful",
                session=session_info
            )
        else:
            logger.warning(f"Login failed for email: {user.email}")
            raise HTTPException(status_code=401, detail="Invalid email or password")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to login: {str(e)}")

@app.post("/logout")
async def logout_user(session_token: str, db=Depends(get_db)):
    """Logout user by invalidating their session"""
    try:
        task_model = TaskModel(db)
        user_id = task_model.validate_session(session_token)
        
        if user_id:
            # Delete the session
            task_model.delete_session(user_id)
            logger.info(f"User logged out successfully: {user_id}")
            return {"message": "Logout successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid session token")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to logout: {str(e)}")

@app.get("/session/validate")
async def validate_session(session_token: str, db=Depends(get_db)):
    """Validate a session token"""
    try:
        task_model = TaskModel(db)
        user_id = task_model.validate_session(session_token)
        
        if user_id:
            logger.info(f"Session validated for user: {user_id}")
            return {"valid": True, "userId": user_id}
        else:
            logger.warning("Invalid session token")
            return {"valid": False, "message": "Invalid or expired session token"}
            
    except Exception as e:
        logger.error(f"Error validating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to validate session: {str(e)}")

@app.get("/stats")
async def get_task_stats(db=Depends(get_db)):
    """Get task statistics"""
    try:
        task_model = TaskModel(db)
        total_tasks = task_model.get_task_count()
        
        # Get tasks by status
        pending_tasks = len(task_model.get_tasks_by_status("pending"))
        in_progress_tasks = len(task_model.get_tasks_by_status("in_progress"))
        completed_tasks = len(task_model.get_tasks_by_status("completed"))
        
        return {
            "total_tasks": total_tasks,
            "pending_tasks": pending_tasks,
            "in_progress_tasks": in_progress_tasks,
            "completed_tasks": completed_tasks
        }
    except Exception as e:
        logger.error(f"Error getting task stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get task stats: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
