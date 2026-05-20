# Requirements — Reminders & Notifications Feature

## Intent Analysis
- **User Request**: Add reminders and in-app notifications to the existing Todo application
- **Request Type**: New Feature (extending brownfield app)
- **Scope**: Multiple Components (backend model extension, new backend service/router, new frontend components)
- **Complexity**: Moderate — new data model, new service, lazy evaluation pattern, polling UI

---

## Functional Requirements

### FR-1: Reminder Time on Todos
- Users can set an optional `reminder_at` datetime (ISO 8601 with timezone) on any todo
- `reminder_at` can be set during creation or update
- `reminder_at` can be cleared (set to null)
- Existing todo CRUD endpoints accept and return the new `reminder_at` field

### FR-2: Notification Data Model
- Notification entity: `{ id, user_id, todo_id, type, message, is_read, created_at }`
- `type` is an enum: `'reminder'` or `'overdue'`
- `id` is a UUID4 string
- `created_at` is ISO 8601 datetime with timezone
- `is_read` defaults to `false`
- Notifications are stored in `data/notifications.json`

### FR-3: Lazy Notification Generation
- When `GET /api/notifications` is called, the server first scans the user's todos for:
  - Todos with `reminder_at <= now` AND status != `'done'` AND no existing reminder notification for that todo
  - Todos with `due_date < today` AND status != `'done'` AND no existing overdue notification for that todo
- New notifications are created for any matching todos before returning the list
- No background scheduler or cron job is used

### FR-4: Notification CRUD Endpoints
- `GET /api/notifications` — returns user's notifications (most recent first), includes `unread_count` in response
- `PATCH /api/notifications/{id}/read` — marks one notification as read
- `POST /api/notifications/read-all` — marks all user's notifications as read
- `DELETE /api/notifications` — permanently deletes all user's notifications

### FR-5: Notification Scoping
- All notification operations are scoped to the authenticated user
- Users cannot see or modify other users' notifications
- Authentication uses existing httpOnly cookie JWT mechanism

### FR-6: Notification Bell UI
- A bell icon appears in the dashboard navbar
- An unread count badge shows the number of unread notifications (hidden when 0)
- Clicking the bell opens a dropdown panel with up to 20 most recent notifications
- Each notification shows: type icon, message text, relative time, read/unread state

### FR-7: Notification Panel Actions
- Mark individual notification as read (click or explicit button)
- "Mark all as read" button
- "Clear all" button (permanently deletes all notifications)
- Clicking a notification navigates focus to the related todo (optional enhancement)

### FR-8: Frontend Polling
- Frontend polls `GET /api/notifications` every 30 seconds
- Polling starts when user is authenticated and on the dashboard
- Polling stops when user logs out or navigates away
- First poll happens immediately on dashboard mount

### FR-9: Reminder Form Integration
- Todo create/edit form includes an optional "Reminder" datetime-local input
- Todo cards display the reminder time when set
- A visual badge/indicator shows when a reminder is upcoming or overdue
- Badge states: "upcoming" (reminder_at in future), "due" (reminder_at passed, not done)

### FR-10: Deduplication
- Only one notification per (todo_id, type) combination is ever created
- If a reminder notification already exists for a todo, no duplicate is created
- If an overdue notification already exists for a todo, no duplicate is created

---

## Non-Functional Requirements

### NFR-1: Performance
- Notification check (lazy scan) must complete within 200ms for typical user (< 100 todos)
- Polling at 30s interval must not degrade backend performance

### NFR-2: Data Consistency
- Atomic writes to notifications.json (using existing JSONStore pattern)
- No data loss on concurrent reads during notification generation

### NFR-3: Compatibility
- No breaking changes to existing todo API responses (additive field only)
- Existing frontend functionality must continue working unchanged

### NFR-4: Simplicity
- No WebSockets, no push notifications, no background workers
- No external dependencies beyond what's already in the project
- JSON file storage (consistent with existing architecture)

---

## Constraints
- Backend: Python FastAPI, extend existing app structure
- Frontend: Nuxt 3 with Vue 3 Composition API, Pinia stores, Tailwind CSS
- Storage: JSON files in `data/` directory (no database)
- Auth: httpOnly cookie JWT (existing mechanism)
- No new infrastructure or deployment changes
