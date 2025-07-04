import sqlite3
from typing import List, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskModel:
    """Task model for database operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_task(self, user_id: int, task_name: str, category: str, time: str, status: str) -> int:
        """Create a new task and return its ID"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                INSERT INTO tasks (userId, taskName, category, time, status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, task_name, category, time, status, datetime.now().isoformat()))
            
            self.db.commit()
            task_id = cursor.lastrowid
            logger.info(f"Created task with ID: {task_id}")
            return task_id
        except sqlite3.Error as e:
            logger.error(f"Error creating task: {str(e)}")
            raise Exception(f"Failed to create task: {str(e)}")
    
    def get_task_by_id(self, task_id: int) -> Optional[Tuple]:
        """Get a task by its ID"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                WHERE taskId = ?
            ''', (task_id,))
            
            result = cursor.fetchone()
            if result:
                return tuple(result)
            return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching task by ID {task_id}: {str(e)}")
            raise Exception(f"Failed to fetch task: {str(e)}")
    
    def update_task(self, task_id: int, user_id: int, task_name: str, category: str, time: str, status: str) -> bool:
        """Update an existing task"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE tasks
                SET userId = ?, taskName = ?, category = ?, time = ?, status = ?, updated_at = ?
                WHERE taskId = ?
            ''', (user_id, task_name, category, time, status, datetime.now().isoformat(), task_id))
            
            self.db.commit()
            
            if cursor.rowcount == 0:
                logger.warning(f"No task found with ID: {task_id}")
                return False
            
            logger.info(f"Updated task with ID: {task_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating task {task_id}: {str(e)}")
            raise Exception(f"Failed to update task: {str(e)}")
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID"""
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM tasks WHERE taskId = ?', (task_id,))
            
            self.db.commit()
            
            if cursor.rowcount == 0:
                logger.warning(f"No task found with ID: {task_id}")
                return False
            
            logger.info(f"Deleted task with ID: {task_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error deleting task {task_id}: {str(e)}")
            raise Exception(f"Failed to delete task: {str(e)}")
    
    def get_all_tasks(self) -> List[Tuple]:
        """Get all tasks sorted by time in descending order"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                ORDER BY time DESC
            ''')
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching all tasks: {str(e)}")
            raise Exception(f"Failed to fetch tasks: {str(e)}")
    
    def get_tasks_by_user(self, user_id: int) -> List[Tuple]:
        """Get all tasks for a specific user sorted by time in descending order"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                WHERE userId = ?
                ORDER BY time DESC
            ''', (user_id,))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching tasks for user {user_id}: {str(e)}")
            raise Exception(f"Failed to fetch user tasks: {str(e)}")
    
    def get_tasks_by_status(self, status: str) -> List[Tuple]:
        """Get all tasks with a specific status sorted by time in descending order"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                WHERE status = ?
                ORDER BY time DESC
            ''', (status,))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching tasks with status {status}: {str(e)}")
            raise Exception(f"Failed to fetch tasks by status: {str(e)}")
    
    def get_tasks_by_category(self, category: str) -> List[Tuple]:
        """Get all tasks in a specific category sorted by time in descending order"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                WHERE category = ?
                ORDER BY time DESC
            ''', (category,))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching tasks with category {category}: {str(e)}")
            raise Exception(f"Failed to fetch tasks by category: {str(e)}")
    
    def get_task_count(self) -> int:
        """Get total number of tasks"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT COUNT(*) FROM tasks')
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error counting tasks: {str(e)}")
            raise Exception(f"Failed to count tasks: {str(e)}")
    
    def get_user_task_count(self, user_id: int) -> int:
        """Get number of tasks for a specific user"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT COUNT(*) FROM tasks WHERE userId = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error counting tasks for user {user_id}: {str(e)}")
            raise Exception(f"Failed to count user tasks: {str(e)}")
