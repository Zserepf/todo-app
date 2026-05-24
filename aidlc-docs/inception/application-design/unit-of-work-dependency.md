# Unit of Work Dependencies — Explicit Contracts

This document defines the EXACT contracts between units. Each contract specifies precise API signatures, request/response JSON shapes, field names, and function signatures. Engineers working on each unit MUST implement these contracts exactly as specified.

---

## Contract 1: Unit 1 → External (HTTP API)

**Provider**: Unit 1 (Notification Backend)
**Consumers**: Unit 3 (Bell UI), Unit 2 (via router integration)

### Endpoint: `GET /api/notifications`

**Authentication**: httpOnly cookie `token` (JWT)

**Request**: No body. No query params.

**Response** (200 OK):
```json
{
  "notifications": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "todo_id": "789e0123-e45b-67d8-a901-234567890000",
      "type": "reminder",
      "message": "Reminder: Buy groceries",
      "is_read": false,
      "created_at": "2026-05-21T14:30:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "user_id": "123e4567-e89b-12d3-a456-426614174000",
      "todo_id": "890e0123-e45b-67d8-a901-234567890001",
      "type": "overdue",
      "message": "Overdue: Submit report",
      "is_read": true,
      "created_at": "2026-05-20T09:00:00Z"
    }
  ],
  "unread_count": 1
}
```

**Response Fields**:
| Field | Type | Description |
|---|---|---|
| `notifications` | array | List of Notification objects, ordered by created_at DESC, max 20 |
| `notifications[].id` | string (UUID4) | Unique notification identifier |
| `notifications[].user_id` | string (UUID4) | Owner user ID |
| `notifications[].todo_id` | string (UUID4) | Related todo ID |
| `notifications[].type` | string enum | `"reminder"` or `"overdue"` |
| `notifications[].message` | string | Human-readable message (e.g., "Reminder: {todo_title}") |
| `notifications[].is_read` | boolean | Whether user has read this notification |
| `notifications[].created_at` | string (ISO 8601) | When notification was created |
| `unread_count` | integer | Total number of unread notifications for this user |

**Error Responses**:
- 401: `{ "detail": "Authentication required" }`

---

### Endpoint: `PATCH /api/notifications/{notification_id}/read`

**Authentication**: httpOnly cookie `token` (JWT)

**Path Parameters**:
| Param | Type | Description |
|---|---|---|
| `notification_id` | string (UUID4) | The notification to mark as read |

**Request**: No body.

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "todo_id": "789e0123-e45b-67d8-a901-234567890000",
  "type": "reminder",
  "message": "Reminder: Buy groceries",
  "is_read": true,
  "created_at": "2026-05-21T14:30:00Z"
}
```

**Error Responses**:
- 401: `{ "detail": "Authentication required" }`
- 404: `{ "detail": "Notification not found" }`

---

### Endpoint: `POST /api/notifications/read-all`

**Authentication**: httpOnly cookie `token` (JWT)

**Request**: No body.

**Response** (200 OK):
```json
{
  "marked_count": 5
}
```

**Response Fields**:
| Field | Type | Description |
|---|---|---|
| `marked_count` | integer | Number of notifications that were marked as read |

**Error Responses**:
- 401: `{ "detail": "Authentication required" }`

---

### Endpoint: `DELETE /api/notifications`

**Authentication**: httpOnly cookie `token` (JWT)

**Request**: No body.

**Response**: 204 No Content (empty body)

**Error Responses**:
- 401: `{ "detail": "Authentication required" }`

---

## Contract 2: Unit 2 → Unit 1 (Internal Python Import)

**Provider**: Unit 1 (NotificationService)
**Consumer**: Unit 2 (ReminderChecker integration in notifications router)

### Function: `notification_service.create()`

**Import Path**: `from services.notification_service import NotificationService`

**Signature**:
```python
def create(self, user_id: str, todo_id: str, notification_type: str, message: str) -> Notification:
    """Create a new notification.
    
    Args:
        user_id: UUID4 string of the notification owner
        todo_id: UUID4 string of the related todo
        notification_type: "reminder" or "overdue"
        message: Human-readable notification message
    
    Returns:
        Notification Pydantic model instance
    
    Side Effects:
        Persists to notifications.json via JSONStore
    """
```

### Function: `notification_service.exists()`

**Signature**:
```python
def exists(self, user_id: str, todo_id: str, notification_type: str) -> bool:
    """Check if a notification already exists for deduplication.
    
    Args:
        user_id: UUID4 string of the notification owner
        todo_id: UUID4 string of the related todo
        notification_type: "reminder" or "overdue"
    
    Returns:
        True if a notification with this (user_id, todo_id, type) exists
    """
```

---

## Contract 3: Unit 1 → Unit 2 (Internal Python Import)

**Provider**: Unit 2 (ReminderChecker)
**Consumer**: Unit 1 (NotificationRouter's GET handler)

### Function: `reminder_checker.check_user()`

**Import Path**: `from services.reminder_checker import check_user`

**Signature**:
```python
def check_user(
    user_id: str,
    todos: list[dict],
    existing_notifications: list[dict]
) -> list[tuple[str, str, str]]:
    """Detect todos that need notifications generated.
    
    Pure function — no I/O, no side effects.
    
    Args:
        user_id: UUID4 string of the user to check
        todos: List of todo dicts for this user. Each dict has keys:
            - "id": str (UUID4)
            - "user_id": str (UUID4)
            - "title": str
            - "status": str ("pending" | "in-progress" | "done")
            - "due_date": str | None (ISO date "YYYY-MM-DD")
            - "reminder_at": str | None (ISO datetime "YYYY-MM-DDTHH:MM:SSZ")
        existing_notifications: List of notification dicts for this user. Each dict has keys:
            - "id": str (UUID4)
            - "user_id": str (UUID4)
            - "todo_id": str (UUID4)
            - "type": str ("reminder" | "overdue")
            - "is_read": bool
    
    Returns:
        List of tuples: [(todo_id, notification_type, message), ...]
        - todo_id: str (UUID4) — the todo that triggered the notification
        - notification_type: str — "reminder" or "overdue"
        - message: str — e.g., "Reminder: Buy groceries" or "Overdue: Submit report"
    
    Logic:
        1. For each todo where reminder_at is set AND reminder_at <= now AND status != "done":
           - If no existing notification with (todo_id, "reminder") exists → add to results
        2. For each todo where due_date is set AND due_date < today AND status != "done":
           - If no existing notification with (todo_id, "overdue") exists → add to results
    """
```

---

## Contract 4: Unit 2 → External (HTTP API — Todo Model Extension)

**Provider**: Unit 2 (Todo model + TodoService)
**Consumer**: Unit 4 (Reminder Form UI)

### Modified Endpoint: `POST /api/todos`

**Request Body** (extended):
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "due_date": "2026-05-25",
  "status": "pending",
  "reminder_at": "2026-05-24T09:00:00Z"
}
```

**New Field**:
| Field | Type | Required | Description |
|---|---|---|---|
| `reminder_at` | string (ISO 8601 datetime) \| null | No | When to trigger reminder notification. Null means no reminder. |

**Response** (201 Created — extended):
```json
{
  "id": "789e0123-e45b-67d8-a901-234567890000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "priority": "medium",
  "due_date": "2026-05-25",
  "status": "pending",
  "reminder_at": "2026-05-24T09:00:00Z",
  "created_at": "2026-05-21T07:00:00Z",
  "updated_at": null
}
```

### Modified Endpoint: `PUT /api/todos/{id}`

**Request Body** (extended):
```json
{
  "reminder_at": "2026-05-24T09:00:00Z"
}
```

Can also set to `null` to clear:
```json
{
  "reminder_at": null
}
```

**Response**: Same as GET /api/todos/{id} with `reminder_at` included.

### Modified Endpoint: `GET /api/todos` and `GET /api/todos/{id}`

**Response** (extended — all todo responses now include):
```json
{
  "id": "...",
  "user_id": "...",
  "title": "...",
  "description": "...",
  "priority": "medium",
  "due_date": "2026-05-25",
  "status": "pending",
  "reminder_at": "2026-05-24T09:00:00Z",
  "created_at": "...",
  "updated_at": null
}
```

**New Field in Response**:
| Field | Type | Description |
|---|---|---|
| `reminder_at` | string (ISO 8601) \| null | Reminder datetime or null if not set |

---

## Contract 5: Unit 3 → Unit 1 (HTTP API)

**Provider**: Unit 1 (Notification Backend HTTP endpoints)
**Consumer**: Unit 3 (Notification Bell UI via `notificationsApi`)

This is the same as Contract 1 above. Unit 3's `useNotifications.ts` composable calls these endpoints:

```typescript
// frontend/utils/api.ts — notificationsApi object

export const notificationsApi = {
  list(): Promise<NotificationsListResponse> {
    // GET /api/notifications
  },
  markAsRead(id: string): Promise<Notification> {
    // PATCH /api/notifications/{id}/read
  },
  markAllAsRead(): Promise<{ marked_count: number }> {
    // POST /api/notifications/read-all
  },
  clearAll(): Promise<void> {
    // DELETE /api/notifications
  },
}
```

**TypeScript Interface** (consumed by Unit 3):
```typescript
// frontend/types/index.ts

export interface Notification {
  id: string
  user_id: string
  todo_id: string
  type: 'reminder' | 'overdue'
  message: string
  is_read: boolean
  created_at: string
}

export interface NotificationsListResponse {
  notifications: Notification[]
  unread_count: number
}
```

---

## Contract 6: Unit 4 → Unit 2 (HTTP API — Todo with reminder_at)

**Provider**: Unit 2 (Todo model extension)
**Consumer**: Unit 4 (Reminder Form UI)

This is the same as Contract 4 above. Unit 4's frontend code sends/receives `reminder_at` via existing todo endpoints.

**TypeScript Interface Extension** (consumed by Unit 4):
```typescript
// frontend/types/index.ts — extend existing Todo interface

export interface Todo {
  id: string
  user_id: string
  title: string
  description: string | null
  priority: 'low' | 'medium' | 'high'
  due_date: string | null
  status: 'pending' | 'in-progress' | 'done'
  reminder_at: string | null  // NEW FIELD
  created_at: string
  updated_at: string | null
}

// TodoCreate and TodoUpdate also get reminder_at: string | undefined
```

---

## Integration Sequence (How Units Connect at Runtime)

```
1. User sets reminder_at on a todo via TodoForm (Unit 4)
2. Frontend sends PUT /api/todos/{id} with reminder_at (Unit 4 → Unit 2's contract)
3. TodoService persists reminder_at to todos.json (Unit 2)
4. 30 seconds later, frontend polls GET /api/notifications (Unit 3 → Unit 1's contract)
5. NotificationRouter reads todos from todo_store (Unit 1)
6. NotificationRouter reads existing notifications from notification_store (Unit 1)
7. NotificationRouter calls reminder_checker.check_user() (Unit 1 → Unit 2's contract)
8. ReminderChecker returns [(todo_id, "reminder", "Reminder: ...")] (Unit 2)
9. NotificationRouter calls notification_service.create() for each result (Unit 1)
10. NotificationRouter returns notifications list + unread_count (Unit 1 → Unit 3's contract)
11. NotificationBell updates badge count (Unit 3)
12. User clicks bell, sees notification in panel (Unit 3)
```

---

## Dependency Graph (Build Order)

```
Unit 1 (Notification Backend) ← no dependencies, can start immediately
Unit 2 (Reminder Trigger)     ← no dependencies, can start immediately
Unit 3 (Bell UI)              ← depends on Unit 1's HTTP API contract (can mock)
Unit 4 (Reminder Form UI)    ← depends on Unit 2's HTTP API contract (can mock)
```

**All 4 units can be developed in parallel** because:
- Unit 1 and Unit 2 have no upstream dependencies
- Unit 3 and Unit 4 depend only on HTTP API contracts which are fully specified above — they can mock the backend during development
- The cross-import between Unit 1 and Unit 2 (`reminder_checker.check_user()` called from `notifications.py`) is resolved at integration time — Unit 1 can stub this call during development

---

## Merge Order (Integration)

1. **Unit 1** merges first (provides notification infrastructure)
2. **Unit 2** merges second (provides reminder_checker + todo model extension)
3. **Unit 3** and **Unit 4** can merge in any order after Units 1 and 2
