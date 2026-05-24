# Code Generation Plan — Unit 1: Notification Backend

## Unit Context

**Unit**: Notification Backend
**Responsibility**: Notification data layer and CRUD endpoints. Manages notification storage, retrieval, and state changes.
**Dependencies**: None (standalone unit)
**Stories Covered**: Notification data model, notification CRUD endpoints, notification scoping, deduplication

## Code Location

- **Workspace Root**: `c:\Users\Elevate\Documents\Learning\kiro\todo-app`
- **Application Code**: `backend/` directory (existing structure)
- **Pattern**: Brownfield — follow existing JSONStore + Service + Router pattern

## Generation Steps

### Step 1: Add Notification Models to `backend/models.py`
- [x] Add `NotificationType` enum (`reminder`, `overdue`)
- [x] Add `Notification` model (id, user_id, todo_id, type, message, is_read, created_at)
- [x] Add `NotificationResponse` model (single notification for API response)
- [x] Add `NotificationsListResponse` model (notifications list + unread_count)

### Step 2: Create `backend/services/notification_service.py`
- [x] Create NotificationService class with JSONStore dependency
- [x] Implement `create(user_id, todo_id, notification_type, message) -> Notification`
- [x] Implement `exists(user_id, todo_id, notification_type) -> bool`
- [x] Implement `list_for_user(user_id) -> list[Notification]` (most recent first, limit 20)
- [x] Implement `get_unread_count(user_id) -> int`
- [x] Implement `mark_read(user_id, notification_id) -> Notification`
- [x] Implement `mark_all_read(user_id) -> int` (returns count marked)
- [x] Implement `delete_all(user_id) -> int` (returns count deleted)

### Step 3: Create `backend/routers/notifications.py`
- [x] Create FastAPI router with prefix `/api/notifications`
- [x] Implement `GET /api/notifications` — returns notifications + unread_count
- [x] Implement `PATCH /api/notifications/{id}/read` — marks one as read
- [x] Implement `POST /api/notifications/read-all` — marks all as read
- [x] Implement `DELETE /api/notifications` — clears all user notifications

### Step 4: Create `backend/data/notifications.json`
- [x] Create empty JSON array file `[]`

### Step 5: Register Router in `backend/main.py`
- [x] Import notifications router
- [x] Register with `app.include_router()`
- [x] Add `PATCH` to CORS allow_methods

### Step 6: Generate Unit Tests for NotificationService
- [x] Create `backend/tests/test_notification_service.py`
- [x] Test `create()` — creates notification with correct fields
- [x] Test `exists()` — returns True/False correctly
- [x] Test `list_for_user()` — returns only user's notifications, sorted by created_at desc
- [x] Test `get_unread_count()` — counts only unread notifications for user
- [x] Test `mark_read()` — marks notification as read, raises NotFoundError if not found/not owned
- [x] Test `mark_all_read()` — marks all user's notifications as read
- [x] Test `delete_all()` — deletes all user's notifications

### Step 7: Generate Code Summary Documentation
- [x] Create `aidlc-docs/construction/unit1-notification-backend/code/code-summary.md`

## Story Traceability

| Story | Covered By Steps |
|---|---|
| Notification Data Model (FR-2) | Step 1 |
| Notification CRUD Endpoints (FR-4) | Steps 2, 3 |
| Notification Scoping (FR-5) | Steps 2, 3 |
| Deduplication (FR-10) | Step 2 (exists method) |

## API Contracts (from unit-of-work.md)

### Endpoints
- `GET /api/notifications` → `{ notifications: [...], unread_count: int }`
- `PATCH /api/notifications/{id}/read` → `{ notification: {...} }`
- `POST /api/notifications/read-all` → `{ message: str, count: int }`
- `DELETE /api/notifications` → `{ message: str, count: int }`

### Internal Interface
- `notification_service.create(user_id, todo_id, notification_type, message) -> Notification`
- `notification_service.exists(user_id, todo_id, notification_type) -> bool`
