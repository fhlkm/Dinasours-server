# Task Management API

## Overview

This is a FastAPI-based task management system that provides REST API endpoints for managing tasks. The application uses SQLite as the database backend and follows a clean architecture pattern with separate modules for database operations, data models, and API schemas.

## System Architecture

The application follows a three-layer architecture:

1. **API Layer (main.py)**: FastAPI application handling HTTP requests and responses
2. **Model Layer (models.py)**: Data access layer with business logic for task operations
3. **Database Layer (database.py)**: SQLite database connection management and initialization

The architecture emphasizes separation of concerns, with dedicated modules for validation (schemas.py) and data access patterns using context managers for safe database operations.

## Key Components

### Database Layer
- **SQLite Database**: Lightweight, file-based database (`tasks.db`)
- **Connection Management**: Context manager pattern for safe database operations
- **Auto-initialization**: Database tables created on application startup

### API Layer
- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Automatic Documentation**: Built-in OpenAPI/Swagger documentation
- **Dependency Injection**: Database connections managed through FastAPI's dependency system

### Data Models
- **Task Model**: Handles CRUD operations for tasks
- **Pydantic Schemas**: Input validation and serialization for API endpoints
- **Type Safety**: Full typing support throughout the application

### Validation
- **Input Validation**: Comprehensive validation for all task fields
- **Status Constraints**: Predefined valid task statuses
- **Data Sanitization**: Automatic trimming of whitespace in text fields

## Data Flow

1. **Request Processing**: FastAPI receives HTTP requests and validates them against Pydantic schemas
2. **Database Operations**: Validated data is passed to TaskModel for database operations
3. **Response Generation**: Results are serialized back to JSON and returned to client
4. **Error Handling**: Exceptions are caught and converted to appropriate HTTP responses

## External Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running the FastAPI application
- **Pydantic**: Data validation and serialization library
- **SQLite3**: Built-in Python database interface (no external database required)

## Deployment Strategy

The application is designed for simple deployment:
- Self-contained SQLite database requires no external database setup
- Single Python application with minimal dependencies
- Can be run locally with `uvicorn main:app --reload`
- Database file (`tasks.db`) is automatically created on first run

## Changelog

- July 04, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.