# Dinasours Task Management API

A FastAPI-based task management system with SQLite database.

## New Endpoint: Get Completed Tasks by Category (This Week)

### Endpoint
```
GET /tasks/user/{user_id}/completed-by-category-this-week
```

### Description
Retrieves the count of completed tasks grouped by category for a specific user for the current week only. This endpoint requires authentication and users can only access their own task statistics.

### Authentication
- **Header**: `Authorization: Bearer {session_token}`
- **Required**: Yes (valid session token)

### Parameters
- `user_id` (path parameter): The ID of the user whose tasks to retrieve

### Response
Returns a list of objects with the following structure:
```json
[
  {
    "category": "work",
    "count": 3
  },
  {
    "category": "personal",
    "count": 2
  },
  {
    "category": "study",
    "count": 1
  }
]
```

### Example Usage
```bash
curl -X GET "https://localhost:8443/tasks/user/abc123-def456-ghi789/completed-by-category-this-week" \
  -H "Authorization: Bearer your_session_token_here"
```

### Security Features
- **User Ownership Verification**: Users can only access their own task statistics
- **Session Validation**: Requires a valid, non-expired session token
- **Authorization Header**: Must include Bearer token for authentication

### Use Cases
- Weekly progress tracking by category
- Current week performance metrics
- Weekly goal achievement tracking
- Personal weekly analytics

### Error Responses
- `401 Unauthorized`: Invalid or missing session token
- `403 Forbidden`: User trying to access another user's data
- `500 Internal Server Error`: Database or server error

## User-Specific Endpoint: Get Completed Tasks by Category for User

### Endpoint
```
GET /tasks/user/{user_id}/completed-by-category
```

### Description
Retrieves the count of completed tasks grouped by category for a specific user. This endpoint requires authentication and users can only access their own task statistics.

### Authentication
- **Header**: `Authorization: Bearer {session_token}`
- **Required**: Yes (valid session token)

### Parameters
- `user_id` (path parameter): The ID of the user whose tasks to retrieve

### Response
Returns a list of objects with the following structure:
```json
[
  {
    "category": "work",
    "count": 5
  },
  {
    "category": "personal",
    "count": 3
  },
  {
    "category": "study",
    "count": 2
  }
]
```

### Example Usage
```bash
curl -X GET "https://localhost:8443/tasks/user/abc123-def456-ghi789/completed-by-category" \
  -H "Authorization: Bearer your_session_token_here"
```

### Security Features
- **User Ownership Verification**: Users can only access their own task statistics
- **Session Validation**: Requires a valid, non-expired session token
- **Authorization Header**: Must include Bearer token for authentication

### Use Cases
- Dashboard analytics showing task completion by category
- Progress tracking across different task categories
- Performance metrics and reporting
- Goal setting and achievement tracking

### Error Responses
- `401 Unauthorized`: Invalid or missing session token
- `403 Forbidden`: User trying to access another user's data
- `500 Internal Server Error`: Database or server error

## Other Available Endpoints

- `POST /task` - Create a new task
- `PUT /task` - Update an existing task
- `DELETE /task/{task_id}` - Delete a task
- `GET /tasks` - Get all tasks
- `GET /tasks/user/{user_id}` - Get tasks for a specific user
- `GET /tasks/user/{user_id}/completed-by-category-this-week` - Get completed task counts by category for a specific user (this week only)
- `POST /register` - Register a new user
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /stats` - Get general task statistics