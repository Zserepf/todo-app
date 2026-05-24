# Integration Test Instructions — Unit 1: Notification Backend

## Purpose
Test the notification endpoints via HTTP to verify router, service, and store work together correctly with authentication.

## Prerequisites
- Backend server running: `python -m uvicorn main:app --port 8000`
- A registered user with valid JWT cookie (use `/api/auth/login` first)

## Test Scenarios

### Scenario 1: List Notifications (Empty State)
- **Endpoint**: `GET /api/notifications`
- **Auth**: Valid JWT cookie
- **Expected Response** (200):
```json
{
  "notifications": [],
  "unread_count": 0
}
```

### Scenario 2: Mark Read (Not Found)
- **Endpoint**: `PATCH /api/notifications/nonexistent-id/read`
- **Auth**: Valid JWT cookie
- **Expected Response** (404):
```json
{
  "detail": "Notification not found"
}
```

### Scenario 3: Mark All Read (Empty State)
- **Endpoint**: `POST /api/notifications/read-all`
- **Auth**: Valid JWT cookie
- **Expected Response** (200):
```json
{
  "message": "All notifications marked as read",
  "count": 0
}
```

### Scenario 4: Delete All (Empty State)
- **Endpoint**: `DELETE /api/notifications`
- **Auth**: Valid JWT cookie
- **Expected Response** (200):
```json
{
  "message": "All notifications cleared",
  "count": 0
}
```

### Scenario 5: Unauthenticated Access
- **Endpoint**: `GET /api/notifications`
- **Auth**: No cookie
- **Expected Response** (401):
```json
{
  "detail": "Authentication required"
}
```

## Manual Integration Test Script

```bash
# 1. Register a user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","password_confirm":"password123"}'

# 2. Login to get cookie
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# 3. List notifications (should be empty)
curl -X GET http://localhost:8000/api/notifications -b cookies.txt

# 4. Mark all read
curl -X POST http://localhost:8000/api/notifications/read-all -b cookies.txt

# 5. Delete all
curl -X DELETE http://localhost:8000/api/notifications -b cookies.txt

# 6. Unauthenticated (should 401)
curl -X GET http://localhost:8000/api/notifications
```

## Notes
- Full integration with notification creation requires Unit 2 (Reminder Trigger Logic)
- Unit 1 endpoints can be tested in isolation for CRUD operations
- Notifications will be created programmatically once Unit 2 is implemented
