import sqlite3
import os
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

DATABASE_PATH = "tasks.db"

def get_connection():
    """Get database connection with proper settings"""
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

def get_db():
    """Dependency for database connections"""
    conn = None
    try:
        conn = get_connection()
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database transaction error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_context():
    """Context manager for database connections"""
    conn = None
    try:
        conn = get_connection()
        yield conn
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database transaction error: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize database with required tables"""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            
            # Create tasks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    taskId INTEGER PRIMARY KEY AUTOINCREMENT,
                    userId BIGINT NOT NULL,
                    taskName TEXT NOT NULL,
                    category TEXT NOT NULL,
                    time TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    userId VARCHAR(30) PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    relationship TEXT NOT NULL,
                    nickname TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    birthday TIMESTAMP,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    sessionId VARCHAR(100) PRIMARY KEY,
                    userId VARCHAR(30) NOT NULL,
                    sessionToken TEXT UNIQUE NOT NULL,
                    expiresAt TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (userId) REFERENCES members(userId) ON DELETE CASCADE
                )
            ''')
            
            # Create index for better performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_id ON tasks(userId)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_time ON tasks(time)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_status ON tasks(status)
            ''')
            
            # Create indexes for members table
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_members_email ON members(email)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_members_relationship ON members(relationship)
            ''')
            
            # Create indexes for sessions table
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sessions_userId ON sessions(userId)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(sessionToken)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expiresAt)
            ''')
            
            conn.commit()
            logger.info("Database tables created successfully")
            
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise Exception(f"Failed to initialize database: {str(e)}")

def check_database_exists():
    """Check if database file exists"""
    return os.path.exists(DATABASE_PATH)

def get_database_info():
    """Get database information for debugging"""
    try:
        with get_db_context() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM tasks")
            task_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            return {
                "database_path": DATABASE_PATH,
                "database_exists": check_database_exists(),
                "task_count": task_count,
                "tables": tables
            }
    except sqlite3.Error as e:
        logger.error(f"Error getting database info: {str(e)}")
        return {"error": str(e)}
