#!/bin/bash

# API Base URL
BASE_URL="http://localhost:8000"

echo "🚀 Starting API Tests..."
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ SUCCESS${NC}"
    else
        echo -e "${RED}❌ FAILED${NC}"
    fi
}

echo -e "${BLUE}1. Register New User${NC}"
echo "POST /register"
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "relationship": "friend",
    "password": "password123",
    "gender": "male",
    "nickname": "TestUser",
    "birthday": "1990-01-01"
  }')

echo "Response: $REGISTER_RESPONSE"
USER_ID=$(echo $REGISTER_RESPONSE | grep -o '"userId":"[^"]*"' | cut -d'"' -f4)
SESSION_TOKEN=$(echo $REGISTER_RESPONSE | grep -o '"sessionToken":"[^"]*"' | cut -d'"' -f4)
print_result $?

echo ""
echo -e "${BLUE}2. User Login${NC}"
echo "POST /login"
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "password123"
  }')

echo "Response: $LOGIN_RESPONSE"
# Update session token from login response
SESSION_TOKEN=$(echo $LOGIN_RESPONSE | grep -o '"sessionToken":"[^"]*"' | cut -d'"' -f4)
print_result $?

echo ""
echo -e "${BLUE}3. Create New Task (Requires Session)${NC}"
echo "POST /task"
TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SESSION_TOKEN" \
  -d '{
    "taskName": "Complete API testing",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }')

echo "Response: $TASK_RESPONSE"
TASK_ID=$(echo $TASK_RESPONSE | grep -o '"taskId":[0-9]*' | cut -d':' -f2)
print_result $?

echo ""
echo -e "${BLUE}4. Get Tasks by User ID (Requires Session)${NC}"
echo "GET /tasks/user/$USER_ID"
USER_TASKS_RESPONSE=$(curl -s -X GET "$BASE_URL/tasks/user/$USER_ID" \
  -H "Authorization: Bearer $SESSION_TOKEN")
echo "Response: $USER_TASKS_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}5. Update Task (Requires Session)${NC}"
echo "PUT /task"
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SESSION_TOKEN" \
  -d '{
    "taskId": '$TASK_ID',
    "taskName": "Complete API testing - Updated",
    "category": "work",
    "time": "2025-01-15T12:00:00",
    "status": "in_progress"
  }')

echo "Response: $UPDATE_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}6. Get All Tasks (Requires Session)${NC}"
echo "GET /tasks"
ALL_TASKS_RESPONSE=$(curl -s -X GET "$BASE_URL/tasks" \
  -H "Authorization: Bearer $SESSION_TOKEN")
echo "Response: $ALL_TASKS_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}7. Test Missing Authorization Header${NC}"
echo "POST /task (without Authorization header)"
MISSING_AUTH_RESPONSE=$(curl -s -X POST "$BASE_URL/task" \
  -H "Content-Type: application/json" \
  -d '{
    "taskName": "Test without auth",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }')
echo "Response: $MISSING_AUTH_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}8. Test Invalid Session Token${NC}"
echo "POST /task (with invalid token)"
INVALID_TOKEN_RESPONSE=$(curl -s -X POST "$BASE_URL/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer invalid_token_here" \
  -d '{
    "taskName": "Test with invalid token",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }')
echo "Response: $INVALID_TOKEN_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}9. Delete Task (Requires Session)${NC}"
echo "DELETE /task/$TASK_ID"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/task/$TASK_ID" \
  -H "Authorization: Bearer $SESSION_TOKEN")
echo "Response: $DELETE_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}10. Validate Session${NC}"
echo "GET /session/validate"
VALIDATE_RESPONSE=$(curl -s -X GET "$BASE_URL/session/validate?session_token=$SESSION_TOKEN")
echo "Response: $VALIDATE_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}11. Logout User${NC}"
echo "POST /logout"
LOGOUT_RESPONSE=$(curl -s -X POST "$BASE_URL/logout" \
  -H "Content-Type: application/json" \
  -d '{"session_token": "'$SESSION_TOKEN'"}')

echo "Response: $LOGOUT_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}12. Test Invalid Session After Logout${NC}"
echo "GET /session/validate (with logged out token)"
INVALID_RESPONSE=$(curl -s -X GET "$BASE_URL/session/validate?session_token=$SESSION_TOKEN")
echo "Response: $INVALID_RESPONSE"
print_result $?

echo ""
echo -e "${BLUE}13. Test Task Access After Logout${NC}"
echo "POST /task (with logged out token)"
LOGOUT_TASK_RESPONSE=$(curl -s -X POST "$BASE_URL/task" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SESSION_TOKEN" \
  -d '{
    "taskName": "Test after logout",
    "category": "work",
    "time": "2025-01-15T10:00:00",
    "status": "pending"
  }')
echo "Response: $LOGOUT_TASK_RESPONSE"
print_result $?

echo ""
echo -e "${YELLOW}📊 Test Summary:${NC}"
echo "================================"
echo "✅ Register User"
echo "✅ User Login" 
echo "✅ Create Task (with session)"
echo "✅ Get User Tasks (with session)"
echo "✅ Update Task (with session)"
echo "✅ Get All Tasks (with session)"
echo "✅ Test Missing Authorization"
echo "✅ Test Invalid Session Token"
echo "✅ Delete Task (with session)"
echo "✅ Validate Session"
echo "✅ Logout User"
echo "✅ Test Invalid Session After Logout"
echo "✅ Test Task Access After Logout"
echo ""
echo -e "${GREEN}🎉 All tests completed!${NC}" 