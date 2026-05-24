# Components

## Backend Components

### 1. Notification Model (`backend/models.py` — extend)
- **Purpose**: Define Pydantic models for Notification entity and API request/response shapes
- **Responsibilities**:
  - `Notification` — internal model with all fields
  - `NotificationResponse` — API response model for a single notification
  - `NotificationsListResponse` — API response wrapping list + unread_count
  - `NotificationType` enum — 'reminder' | 'overdue'
  - Extend `Todo`, `TodoCreate`, `TodoUpdate` with `reminder_at: datetime | None`

### 2. Notification Service (`backend/services/notification_service.py` — new)
- **Purpose**: CRUD operations on notifications scoped to authenticated user
- **Responsibilities**:
  - Create notification (with deduplication check)
  - List user's notifications (most recent first, limit 20)
  - Count unread notifications
  - Mark single notification as read
  - Mark all user's notifications as read
  - Delete all user's notifications

### 3. Reminder Checker (`backend/services/reminder_checker.py` — new)
- **Purpose**: Pure logic for detecting due reminders and overdue todos
- **Responsibilities**:
  - Scan user's todos for reminder_at <= now (not done, no existing notification)
  - Scan user's todos for due_date < today (not done, no existing notification)
  - Return list of (todo_id, type, message) tuples for notifications to create
  - No side effects — caller is responsible for creating notifications

### 4. Notification Router (`backend/routers/notifications.py` — new)
- **Purpose**: HTTP endpoint layer for notification operations
- **Responsibilities**:
  - `GET /api/notifications` — trigger reminder check, then return notifications
  - `PATCH /api/notifications/{id}/read` — mark one as read
  - `POST /api/notifications/read-all` — mark all as read
  - `DELETE /api/notifications` — clear all
  - All endpoints require authentication via `get_current_user` dependency

### 5. Todo Service Extension (`backend/services/todo_service.py` — modify)
- **Purpose**: Support `reminder_at` field in todo CRUD
- **Responsibilities**:
  - Accept `reminder_at` in create and update operations
  - Validate `reminder_at` format (ISO 8601 datetime)
  - Return `reminder_at` in todo responses

---

## Frontend Components

### 6. NotificationBell (`frontend/components/NotificationBell.vue` — new)
- **Purpose**: Bell icon with unread count badge in the navbar
- **Responsibilities**:
  - Display bell SVG icon
  - Show/hide numeric badge based on unread count
  - Toggle notification panel on click
  - Accessible (aria-label, keyboard support)

### 7. NotificationPanel (`frontend/components/NotificationPanel.vue` — new)
- **Purpose**: Dropdown panel showing recent notifications
- **Responsibilities**:
  - Display list of up to 20 notifications
  - Show type icon, message, relative time for each
  - Visual distinction between read/unread
  - "Mark all as read" button
  - "Clear all" button
  - Empty state when no notifications
  - Close on outside click or Escape key

### 8. useNotifications Composable (`frontend/composables/useNotifications.ts` — new)
- **Purpose**: Notification state management and polling logic
- **Responsibilities**:
  - Reactive state: notifications list, unread count, loading
  - Fetch notifications from API
  - 30-second polling interval (start/stop lifecycle)
  - Mark as read (single and all)
  - Clear all notifications
  - Expose state and actions to components

### 9. ReminderBadge (`frontend/components/ReminderBadge.vue` — new)
- **Purpose**: Visual indicator for reminder status on todo cards
- **Responsibilities**:
  - Show "upcoming" badge (neutral/info style) when reminder_at is in the future
  - Show "due" badge (warning style) when reminder_at has passed and todo not done
  - Hidden when reminder_at is null

### 10. TodoForm Extension (`frontend/components/TodoForm.vue` — modify)
- **Purpose**: Add reminder datetime input to create/edit form
- **Responsibilities**:
  - datetime-local input for reminder_at
  - Clear button to remove reminder
  - Include reminder_at in form submission data

### 11. TodoCard Extension (`frontend/components/TodoItem.vue` — modify)
- **Purpose**: Display reminder info and badge on todo cards
- **Responsibilities**:
  - Show formatted reminder_at datetime
  - Include ReminderBadge component
