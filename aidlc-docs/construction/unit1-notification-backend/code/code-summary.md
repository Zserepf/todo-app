# Code Summary — Unit 1: Notification Backend

## Files Modified

| File | Change |
|---|---|
| `backend/models.py` | Added NotificationType enum, Notification, NotificationResponse, NotificationsListResponse models |
| `backend/main.py` | Imported and registered notifications router; added PATCH to CORS allow_methods |

## Files Created

| File | Purpose |
|---|---|
| `backend/services/notification_service.py` | NotificationService class with CRUD operations |
| `backend/routers/notifications.py` | FastAPI router with 4 notification endpoints |
| `backend/data/notifications.json` | Empty JSON array for notification storage |
| `backend/tests/test_notification_service.py` | 24 unit tests covering all service methods |

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/api/notifications` | List user's notifications + unread_count |
| PATCH | `/api/notifications/{id}/read` | Mark one notification as read |
| POST | `/api/notifications/read-all` | Mark all notifications as read |
| DELETE | `/api/notifications` | Delete all user's notifications |

## Internal Interface (for Unit 2 integration)

```python
notification_service.create(user_id, todo_id, notification_type, message) -> Notification
notification_service.exists(user_id, todo_id, notification_type) -> bool
```

## Design Decisions

- Follows existing JSONStore → Service → Router pattern
- All operations scoped to authenticated user via `get_current_user` dependency
- Deduplication via `exists()` method checking (user_id, todo_id, type) tuple
- Notifications limited to 20 most recent per list request
- Atomic writes via JSONStore's temp-file-and-replace pattern
