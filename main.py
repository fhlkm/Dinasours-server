from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
from database import get_db, init_db
from models import TaskModel
from schemas import TaskCreate, TaskUpdate, TaskResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Management API",
    description="A FastAPI-based task management system with SQLite database",
    version="1.0.0"
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

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
async def create_task(task: TaskCreate, db=Depends(get_db)):
    """Create a new task"""
    try:
        task_model = TaskModel(db)
        task_id = task_model.create_task(
            user_id=task.userId,
            task_name=task.taskName,
            category=task.category,
            time=task.time,
            status=task.status
        )
        
        # Retrieve the created task
        created_task = task_model.get_task_by_id(task_id)
        if not created_task:
            raise HTTPException(status_code=500, detail="Failed to retrieve created task")
        
        logger.info(f"Task created successfully with ID: {task_id}")
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
async def update_task(task: TaskUpdate, db=Depends(get_db)):
    """Update an existing task"""
    try:
        task_model = TaskModel(db)
        
        # Check if task exists
        existing_task = task_model.get_task_by_id(task.taskId)
        if not existing_task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task.taskId} not found")
        
        # Update task
        success = task_model.update_task(
            task_id=task.taskId,
            user_id=task.userId,
            task_name=task.taskName,
            category=task.category,
            time=task.time,
            status=task.status
        )
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update task")
        
        # Retrieve updated task
        updated_task = task_model.get_task_by_id(task.taskId)
        logger.info(f"Task updated successfully with ID: {task.taskId}")
        
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
async def delete_task(task_id: int, db=Depends(get_db)):
    """Delete a task by ID"""
    try:
        task_model = TaskModel(db)
        
        # Check if task exists
        existing_task = task_model.get_task_by_id(task_id)
        if not existing_task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        
        # Delete task
        success = task_model.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete task")
        
        logger.info(f"Task deleted successfully with ID: {task_id}")
        return {"message": f"Task with ID {task_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")

@app.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks(db=Depends(get_db)):
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
        
        logger.info(f"Retrieved {len(task_list)} tasks")
        return task_list
    except Exception as e:
        logger.error(f"Error retrieving tasks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")

@app.get("/tasks/user/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks(user_id: int, db=Depends(get_db)):
    """Get all tasks for a specific user sorted by time in descending order"""
    try:
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
    except Exception as e:
        logger.error(f"Error retrieving tasks for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks for user: {str(e)}")

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
