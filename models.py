import sqlite3
from typing import List, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class TaskModel:
    """Task model for database operations"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def create_task(self, user_id: str, task_name: str, category: str, time: str, status: str) -> int:
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
    
    def update_task(self, task_id: int, user_id: str, task_name: str, category: str, time: str, status: str) -> bool:
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
            raise Exception(f"Failed to fetch all tasks: {str(e)}")
    
    def get_all_tasks_paginated(self, offset: int = 0, limit: int = 20) -> List[Tuple]:
        """Get all tasks with pagination sorted by time in descending order"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                ORDER BY time DESC
                LIMIT ? OFFSET ?
            ''', (limit, offset))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching paginated tasks: {str(e)}")
            raise Exception(f"Failed to fetch paginated tasks: {str(e)}")
    
    def get_tasks_by_user_paginated(self, user_id: str, offset: int = 0, limit: int = 20) -> List[Tuple]:
        """Get paginated tasks for a specific user sorted by time in descending order"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                WHERE userId = ?
                ORDER BY time DESC
                LIMIT ? OFFSET ?
            ''', (user_id, limit, offset))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching paginated tasks for user {user_id}: {str(e)}")
            raise Exception(f"Failed to fetch paginated user tasks: {str(e)}")
    
    def get_tasks_by_user(self, user_id: str) -> List[Tuple]:
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
    
    def get_user_task_count(self, user_id: str) -> int:
        """Get number of tasks for a specific user"""
        try:
            cursor = self.db.cursor()
            cursor.execute('SELECT COUNT(*) FROM tasks WHERE userId = ?', (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error counting tasks for user {user_id}: {str(e)}")
            raise Exception(f"Failed to count user tasks: {str(e)}")
    
    def add_new_member(self, email: str, relationship: str, password: str, gender: str, nickname: str, birth: str) -> str:
        """Add a new member to the database and return the user ID"""
        try:
            cursor = self.db.cursor()
            
            # Generate a unique user ID (you might want to implement a more sophisticated ID generation)
            import uuid
            user_id = str(uuid.uuid4())[:30]  # Limit to 30 characters as per schema
            
            cursor.execute('''
                INSERT INTO members (userId, email, relationship, nickname, gender, birthday, password, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, email, relationship, nickname, gender, birth, password, datetime.now().isoformat()))
            
            self.db.commit()
            logger.info(f"Created new member with user ID: {user_id}")
            return user_id
        except sqlite3.IntegrityError as e:
            logger.error(f"Integrity error creating member: {str(e)}")
            raise Exception(f"Failed to create member - email might already exist: {str(e)}")
        except sqlite3.Error as e:
            logger.error(f"Error creating member: {str(e)}")
            raise Exception(f"Failed to create member: {str(e)}")
    
    def getUser(self, email: str, password: str) -> Optional[str]:
        """Get user ID by validating email and password"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT userId
                FROM members
                WHERE email = ? AND password = ?
            ''', (email, password))
            
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                logger.info(f"User authenticated successfully: {user_id}")
                return user_id
            else:
                logger.warning(f"email or password is incorrect")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error authenticating user with email {email}: {str(e)}")
            raise Exception(f"Failed to authenticate user: {str(e)}")
    
    def create_session(self, user_id: str) -> dict:
        """Create a new session for a user and return session info"""
        try:
            cursor = self.db.cursor()
            
            # Generate unique session ID and token
            import uuid
            import jwt
            import time
            
            session_id = str(uuid.uuid4())
            session_token = jwt.encode(
                {
                    'user_id': user_id,
                    'session_id': session_id,
                    'exp': int(time.time()) + (24 * 60 * 60*365*5)  # 24*365*5 hours from now
                },
                'your-secret-key',  # In production, use environment variable
                algorithm='HS256'
            )
            
            # Calculate expiration time (5 years from now)
            from datetime import datetime, timedelta
            expires_at = (datetime.now() + timedelta(hours=24*365*5)).isoformat()
            
            # Delete any existing sessions for this user
            cursor.execute('DELETE FROM sessions WHERE userId = ?', (user_id,))
            
            # Insert new session
            cursor.execute('''
                INSERT INTO sessions (sessionId, userId, sessionToken, expiresAt)
                VALUES (?, ?, ?, ?)
            ''', (session_id, user_id, session_token, expires_at))
            
            self.db.commit()
            logger.info(f"Created new session for user: {user_id}")
            
            return {
                "sessionToken": session_token,
                "expiresAt": expires_at
            }
        except sqlite3.Error as e:
            logger.error(f"Error creating session for user {user_id}: {str(e)}")
            raise Exception(f"Failed to create session: {str(e)}")
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate a session token and return user ID if valid"""
        try:
            cursor = self.db.cursor()
            
            # Check if session exists and is not expired
            cursor.execute('''
                SELECT userId
                FROM sessions
                WHERE sessionToken = ? AND expiresAt > ?
            ''', (session_token, datetime.now().isoformat()))
            
            result = cursor.fetchone()
            if result:
                user_id = result[0]
                logger.info(f"Session validated for user: {user_id}")
                return user_id
            else:
                logger.warning("Invalid or expired session token")
                return None
        except sqlite3.Error as e:
            logger.error(f"Error validating session: {str(e)}")
            raise Exception(f"Failed to validate session: {str(e)}")
    
    def delete_session(self, user_id: str) -> bool:
        """Delete all sessions for a user"""
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM sessions WHERE userId = ?', (user_id,))
            self.db.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Deleted sessions for user: {user_id}")
                return True
            else:
                logger.warning(f"No sessions found for user: {user_id}")
                return False
        except sqlite3.Error as e:
            logger.error(f"Error deleting sessions for user {user_id}: {str(e)}")
            raise Exception(f"Failed to delete sessions: {str(e)}")
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return number of deleted sessions"""
        try:
            cursor = self.db.cursor()
            cursor.execute('DELETE FROM sessions WHERE expiresAt <= ?', (datetime.now().isoformat(),))
            deleted_count = cursor.rowcount
            self.db.commit()
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired sessions")
            
            return deleted_count
        except sqlite3.Error as e:
            logger.error(f"Error cleaning up expired sessions: {str(e)}")
            raise Exception(f"Failed to cleanup sessions: {str(e)}")
    
    def get_user_by_id(self, user_id: str) -> Optional[Tuple]:
        """Get user details by user ID"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT userId, email, relationship, nickname, gender, birthday
                FROM members
                WHERE userId = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if result:
                return tuple(result)
            return None
        except sqlite3.Error as e:
            logger.error(f"Error fetching user by ID {user_id}: {str(e)}")
            raise Exception(f"Failed to fetch user: {str(e)}")

    def get_user_tasks_by_month(self, user_id: str, year: int, month: int) -> List[Tuple]:
        """Get all tasks for a specific user in a specific month"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT taskId, userId, taskName, category, time, status
                FROM tasks
                WHERE userId = ? AND strftime('%Y', time) = ? AND strftime('%m', time) = ?
                ORDER BY time DESC
            ''', (user_id, str(year), f"{month:02d}"))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching tasks for user {user_id} in {year}-{month:02d}: {str(e)}")
            raise Exception(f"Failed to fetch user tasks by month: {str(e)}")

    def get_completed_tasks_by_category_for_user(self, user_id: str) -> List[Tuple]:
        """Get count of completed tasks by category for a specific user"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM tasks
                WHERE userId = ? AND status = 'completed'
                GROUP BY category
                ORDER BY count DESC
            ''', (user_id,))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching completed tasks by category for user {user_id}: {str(e)}")
            raise Exception(f"Failed to fetch completed tasks by category: {str(e)}")

    def get_completed_tasks_by_category_all_users(self) -> List[Tuple]:
        """Get count of completed tasks by category across all users"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM tasks
                WHERE status = 'completed'
                GROUP BY category
                ORDER BY count DESC
            ''')
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching completed tasks by category for all users: {str(e)}")
            raise Exception(f"Failed to fetch completed tasks by category for all users: {str(e)}")

    def get_completed_tasks_by_category_this_week_for_user(self, user_id: str) -> List[Tuple]:
        """Get count of completed tasks by category for a specific user for the current week"""
        try:
            cursor = self.db.cursor()
            cursor.execute('''
                SELECT category, COUNT(*) as count
                FROM tasks
                WHERE userId = ? AND status = 'completed' 
                AND strftime('%Y-%W', time) = strftime('%Y-%W', 'now')
                GROUP BY category
                ORDER BY count DESC
            ''', (user_id,))
            
            results = cursor.fetchall()
            return [tuple(row) for row in results]
        except sqlite3.Error as e:
            logger.error(f"Error fetching completed tasks by category for user {user_id} this week: {str(e)}")
            raise Exception(f"Failed to fetch completed tasks by category this week: {str(e)}")
