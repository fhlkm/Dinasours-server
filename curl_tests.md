# API Testing with cURL

## Base URL
```
http://localhost:8000
```

## Authentication Flow
All task operations now require a valid session token in the Authorization header:
```
Authorization: Bearer <session_token>
```

## 1. Register New User
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "relationship": "friend",
    "password": "password123",
    "gender": "male",
    "nickname": "TestUser",
    "birthday": "1990-01-01"
  }'
```

**Expected Response:**
```json
{
  "userId": "abc123-def456-ghi789",
  "message": "User registered successfully",
  "session": {
    "sessionToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2030-01-15T10:00:00Z"
  }
}
```

## 2. User Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "password123"
  }'
```

**Expected Response:**
```json
{
  "userId": "abc123-def456-ghi789",
  "message": "Login successful",
  "session": {
    "sessionToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expiresAt": "2030-01-15T10:00:00Z"
  }
}
```

## 3. Create New Task (Requires Session)
```bash
curl -X POST "http://localhost:8000/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "taskName": "Complete API testing",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }'
```

**Expected Response:**
```json
{
  "taskId": 1,
  "userId": "abc123-def456-ghi789",
  "taskName": "Complete API testing",
  "category": "work",
  "time": "2025-01-15T10:00:00",
  "status": "pending"
}
```

## 4. Get Tasks by User ID (Requires Session)
```bash
curl -X GET "http://localhost:8000/tasks/user/abc123-def456-ghi789" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
[
  {
    "taskId": 1,
    "userId": "abc123-def456-ghi789",
    "taskName": "Complete API testing",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }
]
```

## 5. Update Task (Requires Session)
```bash
curl -X PUT "http://localhost:8000/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{
    "taskId": 1,
    "taskName": "Complete API testing - Updated",
    "category": "work",
    "time": "2025-01-15T12:00:00",
    "status": "in_progress"
  }'
```

**Expected Response:**
```json
{
  "taskId": 1,
  "userId": "abc123-def456-ghi789",
  "taskName": "Complete API testing - Updated",
  "category": "work",
  "time": "2025-01-15T12:00:00",
  "status": "in_progress"
}
```

## 6. Get All Tasks (Requires Session)
```bash
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
[
  {
    "taskId": 1,
    "userId": "abc123-def456-ghi789",
    "taskName": "Complete API testing - Updated",
    "category": "work",
    "time": "2025-01-15T12:00:00",
    "status": "in_progress"
  }
]
```

## 7. Delete Task (Requires Session)
```bash
curl -X DELETE "http://localhost:8000/task/1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
{
  "message": "Task with ID 1 deleted successfully"
}
```

## 8. Validate Session
```bash
curl -X GET "http://localhost:8000/session/validate?session_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
{
  "valid": true,
  "userId": "abc123-def456-ghi789"
}
```

## 9. Logout User
```bash
curl -X POST "http://localhost:8000/logout" \
  -H "Content-Type: application/json" \
  -d '{
    "session_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

**Expected Response:**
```json
{
  "message": "Logout successful"
}
```

## 10. Test Invalid Session After Logout
```bash
curl -X GET "http://localhost:8000/session/validate?session_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Expected Response:**
```json
{
  "valid": false,
  "message": "Invalid or expired session token"
}
```

## Error Cases

### Missing Authorization Header
```bash
curl -X POST "http://localhost:8000/task" \
  -H "Content-Type: application/json" \
  -d '{
    "taskName": "Complete API testing",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }'
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Valid session token is required"
}
```

### Invalid Session Token
```bash
curl -X POST "http://localhost:8000/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token" \
  -d '{
    "taskName": "Complete API testing",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }'
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Session expired or invalid"
}
```

### Task Ownership Violation
```bash
# Try to update another user's task
curl -X PUT "http://localhost:8000/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer user1_session_token" \
  -d '{
    "taskId": 5,
    "taskName": "Hack attempt",
    "category": "work",
    "time": "2025-01-15T12:00:00",
    "status": "in_progress"
  }'
```

**Expected Response (403 Forbidden):**
```json
{
  "detail": "You can only update your own tasks"
}
```

### Access Another User's Tasks
```bash
# Try to access another user's tasks
curl -X GET "http://localhost:8000/tasks/user/other_user_id" \
  -H "Authorization: Bearer user1_session_token"
```

**Expected Response (403 Forbidden):**
```json
{
  "detail": "You can only access your own tasks"
}
```

### Duplicate Email Registration
```bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "relationship": "friend",
    "password": "password123",
    "gender": "male",
    "nickname": "TestUser",
    "birthday": "1990-01-01"
  }'
```

**Expected Response (409 Conflict):**
```json
{
  "detail": "Email already exists"
}
```

### Invalid Login
```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "wrongpassword"
  }'
```

**Expected Response (401 Unauthorized):**
```json
{
  "detail": "Invalid email or password"
}
```

### Get Task Statistics
```bash
curl -X GET "http://localhost:8000/stats"
```

**Expected Response:**
```json
{
  "total_tasks": 0,
  "pending_tasks": 0,
  "in_progress_tasks": 0,
  "completed_tasks": 0
}
```

## Security Features

### ✅ Session-Based Authentication
- All task operations require valid session tokens
- Session tokens are validated on every request
- Users can only access their own tasks

### ✅ Task Ownership Protection
- Users can only update/delete their own tasks
- Users can only view their own tasks (except admin view)
- Ownership is verified before any operation

### ✅ Session Management
- Sessions expire after 5 years
- Logout invalidates sessions immediately
- One session per user (new login replaces old session)

### ✅ Error Handling
- Clear error messages for authentication failures
- Proper HTTP status codes (401, 403, 409)
- Detailed logging for security monitoring 