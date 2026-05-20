# Component Methods

## NotificationService

### `create(user_id: str, todo_id: str, notification_type: str, message: str) -> Notification`
- Creates a new notification record
- Generates UUID, sets created_at to now, is_read=False
- Persists to notifications.json via JSONStore
- Returns the created Notification

### `list_notifications(user_id: str, limit: int = 20) -> list[Notification]`
- Reads all notifications for user_id
- Sorts by created_at descending (most recent first)
- Returns up to `limit` notifications

### `get_unread_count(user_id: str) -> int`
- Counts notifications where user_id matches and is_read=False
- Returns integer count

### `mark_as_read(user_id: str, notification_id: str) -> Notification`
- Finds notification by id, verifies user_id ownership
- Sets is_read=True
- Persists change
- Raises NotFoundError if not found or not owned

### `mark_all_as_read(user_id: str) -> int`
- Finds all notifications for user_id where is_read=False
- Sets is_read=True on all
- Persists changes
- Returns count of notifications marked

### `delete_all(user_id: str) -> int`
- Removes all notifications for user_id from store
- Persists changes
- Returns count of notifications deleted

### `exists(user_id: str, todo_id: str, notification_type: str) -> bool`
- Checks if a notification already exists for (user_id, todo_id, type)
- Used for deduplication
- Returns boolean

---

## ReminderChecker

### `check_user(user_id: str, todos: list[dict], existing_notifications: list[dict]) -> list[tuple[str, str, str]]`
- Pure function — no side effects, no I/O
- Parameters:
  - `user_id`: the user to check for
  - `todos`: list of todo dicts for this user (from todo_store)
  - `existing_notifications`: list of notification dicts for this user (from notification_store)
- Logic:
  - For each todo where `reminder_at` is set, `reminder_at <= now`, `status != 'done'`:
    - Check if notification with (todo_id, 'reminder') exists in existing_notifications
    - If not, add `(todo_id, 'reminder', f"Reminder: {todo['title']}")` to results
  - For each todo where `due_date` is set, `due_date < today`, `status != 'done'`:
    - Check if notification with (todo_id, 'overdue') exists in existing_notifications
    - If not, add `(todo_id, 'overdue', f"Overdue: {todo['title']}")` to results
- Returns: list of `(todo_id, type, message)` tuples

---

## NotificationRouter

### `GET /api/notifications`
- Calls `reminder_checker.check_user()` to detect new notifications
- Creates any new notifications via `notification_service.create()`
- Returns `NotificationsListResponse` with notifications + unread_count

### `PATCH /api/notifications/{notification_id}/read`
- Calls `notification_service.mark_as_read()`
- Returns updated notification

### `POST /api/notifications/read-all`
- Calls `notification_service.mark_all_as_read()`
- Returns `{ "marked_count": N }`

### `DELETE /api/notifications`
- Calls `notification_service.delete_all()`
- Returns 204 No Content

---

## TodoService Extensions

### Modified: `create(user_id, data) -> Todo`
- Now accepts `reminder_at` from TodoCreate
- Validates reminder_at format if provided (ISO 8601 datetime)
- Stores reminder_at in todo record

### Modified: `update(user_id, todo_id, data) -> Todo`
- Now accepts `reminder_at` from TodoUpdate
- Validates reminder_at format if provided
- Can set reminder_at to null (clear reminder)

---

## Frontend: useNotifications Composable

### `fetchNotifications() -> void`
- Calls `GET /api/notifications`
- Updates reactive state: notifications, unreadCount

### `markAsRead(id: string) -> void`
- Calls `PATCH /api/notifications/{id}/read`
- Updates local state optimistically

### `markAllAsRead() -> void`
- Calls `POST /api/notifications/read-all`
- Updates local state: all notifications set to read, unreadCount = 0

### `clearAll() -> void`
- Calls `DELETE /api/notifications`
- Clears local state: notifications = [], unreadCount = 0

### `startPolling() -> void`
- Sets up 30-second interval calling fetchNotifications
- Calls fetchNotifications immediately

### `stopPolling() -> void`
- Clears the interval
