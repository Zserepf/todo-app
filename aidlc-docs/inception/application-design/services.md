# Services

## Service Architecture

The notification feature follows the existing service-layer pattern in the codebase:
- **Router** → **Service** → **Store (JSONStore)**
- Services contain business logic; routers handle HTTP concerns; stores handle persistence.

---

## NotificationService

- **Type**: Application Service
- **Instantiation**: Singleton, created at module level in `routers/notifications.py` (same pattern as TodoService)
- **Dependencies**: `JSONStore` instance for `data/notifications.json`
- **Responsibility**: All CRUD operations on notifications, scoped to user_id
- **Pattern**: Same as existing `TodoService` — constructor receives store, methods take user_id as first param

---

## ReminderChecker

- **Type**: Domain Logic (pure functions)
- **Instantiation**: Stateless module with a single function `check_user()`
- **Dependencies**: None (receives data as parameters)
- **Responsibility**: Detect which todos need notifications generated
- **Pattern**: Pure function — no I/O, no store access, fully testable in isolation
- **Called by**: Notification router's `GET /api/notifications` handler

---

## TodoService (Extended)

- **Type**: Application Service (existing, modified)
- **Changes**: Accept and persist `reminder_at` field in create/update operations
- **No new dependencies**: Uses same `JSONStore` instance

---

## Service Orchestration Flow

```
GET /api/notifications request
    |
    v
NotificationRouter.list_notifications()
    |
    |-- 1. Read user's todos from todo_store
    |-- 2. Read user's existing notifications from notification_store
    |-- 3. Call reminder_checker.check_user(user_id, todos, notifications)
    |-- 4. For each result tuple, call notification_service.create(...)
    |-- 5. Call notification_service.list_notifications(user_id)
    |-- 6. Call notification_service.get_unread_count(user_id)
    |-- 7. Return NotificationsListResponse
    v
Response: { notifications: [...], unread_count: N }
```

---

## Store Instances

| Store | File Path | Used By |
|---|---|---|
| `user_store` | `data/users.json` | AuthService (existing) |
| `todo_store` | `data/todos.json` | TodoService (existing) |
| `notification_store` | `data/notifications.json` | NotificationService (new) |
