# Application Design — Reminders & Notifications

## Overview

This feature extends the existing Todo application with reminder scheduling and in-app notifications. The design follows the established patterns in the codebase:
- **Backend**: FastAPI router → Service → JSONStore
- **Frontend**: Vue component → Composable → API utility → Backend

## Architecture Approach

**Lazy evaluation pattern**: No background scheduler. Notification generation happens on-demand when the frontend polls `GET /api/notifications`. The backend scans for due reminders and overdue todos at that moment, creates any missing notifications, then returns the list.

**Polling pattern**: Frontend polls every 30 seconds. Simple, reliable, no WebSocket complexity.

**Deduplication**: Each (todo_id, notification_type) pair can only produce one notification. Prevents duplicate alerts on repeated polls.

---

## New Backend Components

| Component | File | Type |
|---|---|---|
| Notification models | `backend/models.py` (extend) | Pydantic models |
| NotificationService | `backend/services/notification_service.py` (new) | Application service |
| ReminderChecker | `backend/services/reminder_checker.py` (new) | Pure domain logic |
| NotificationRouter | `backend/routers/notifications.py` (new) | HTTP endpoints |
| TodoService extension | `backend/services/todo_service.py` (modify) | Add reminder_at support |
| Main app registration | `backend/main.py` (modify) | Register new router |

## New Frontend Components

| Component | File | Type |
|---|---|---|
| NotificationBell | `frontend/components/NotificationBell.vue` (new) | UI component |
| NotificationPanel | `frontend/components/NotificationPanel.vue` (new) | UI component |
| ReminderBadge | `frontend/components/ReminderBadge.vue` (new) | UI component |
| useNotifications | `frontend/composables/useNotifications.ts` (new) | Composable |
| Notification types | `frontend/types/index.ts` (extend) | TypeScript interfaces |
| Notifications API | `frontend/utils/api.ts` (extend) | API client |
| TodoForm extension | `frontend/components/TodoForm.vue` (modify) | Add reminder input |
| TodoItem extension | `frontend/components/TodoItem.vue` (modify) | Show reminder badge |
| Dashboard extension | `frontend/pages/dashboard.vue` (modify) | Add bell to navbar |

---

## API Contract Summary

| Method | Path | Purpose |
|---|---|---|
| GET | /api/notifications | List notifications (triggers lazy check) |
| PATCH | /api/notifications/{id}/read | Mark one as read |
| POST | /api/notifications/read-all | Mark all as read |
| DELETE | /api/notifications | Clear all notifications |

All existing `/api/todos` endpoints now accept/return `reminder_at` field (additive, non-breaking).

---

## Key Design Decisions

1. **Pure function for detection**: `ReminderChecker.check_user()` takes data as params, returns tuples. No I/O. Easy to test.
2. **Deduplication via existence check**: Before creating a notification, check if (todo_id, type) already exists.
3. **Atomic JSON writes**: Reuse existing `JSONStore._write_atomic()` pattern for notifications.json.
4. **Composable pattern**: `useNotifications` manages polling lifecycle, matching existing `useTodos` pattern.
5. **No store (Pinia)**: Notifications use a composable directly (simpler than a full Pinia store for this use case).

---

## Detailed Design References

- **Components**: See `components.md`
- **Methods**: See `component-methods.md`
- **Services**: See `services.md`
- **Dependencies**: See `component-dependency.md`
- **Units of Work**: See `unit-of-work.md`
- **Contracts**: See `unit-of-work-dependency.md`
