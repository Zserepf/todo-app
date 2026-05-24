# Unit of Work — Story Map

## Story-to-Unit Assignment

| Story ID | Story Title | Primary Unit | Supporting Unit(s) |
|---|---|---|---|
| US-1 | Set Reminder on Todo | Unit 4 (Form UI) | Unit 2 (Backend model) |
| US-2 | View Reminder on Todo Card | Unit 4 (Form UI) | — |
| US-3 | Generate Reminder Notifications | Unit 2 (Trigger Logic) | Unit 1 (creates notifications) |
| US-4 | Generate Overdue Notifications | Unit 2 (Trigger Logic) | Unit 1 (creates notifications) |
| US-5 | View Notifications via Bell Icon | Unit 3 (Bell UI) | Unit 1 (API) |
| US-6 | View Notification Panel | Unit 3 (Bell UI) | Unit 1 (API) |
| US-7 | Mark Notification as Read | Unit 3 (Bell UI) | Unit 1 (API) |
| US-8 | Mark All as Read | Unit 3 (Bell UI) | Unit 1 (API) |
| US-9 | Clear All Notifications | Unit 3 (Bell UI) | Unit 1 (API) |
| US-10 | Automatic Polling | Unit 3 (Bell UI) | Unit 1 (API) |

---

## Unit 1: Notification Backend — Stories

| Story | Responsibility in this Unit |
|---|---|
| US-3 | Provide `notification_service.create()` called during GET /api/notifications |
| US-4 | Provide `notification_service.create()` called during GET /api/notifications |
| US-5 | Provide `GET /api/notifications` returning unread_count |
| US-6 | Provide `GET /api/notifications` returning notification list |
| US-7 | Provide `PATCH /api/notifications/{id}/read` endpoint |
| US-8 | Provide `POST /api/notifications/read-all` endpoint |
| US-9 | Provide `DELETE /api/notifications` endpoint |
| US-10 | Provide `GET /api/notifications` endpoint (polled by frontend) |

**Acceptance Criteria owned by Unit 1**:
- Notification CRUD operations work correctly
- Notifications are scoped to authenticated user
- Responses match exact JSON shapes in `unit-of-work-dependency.md`
- Deduplication check works (exists method)
- Atomic writes to notifications.json

---

## Unit 2: Reminder Trigger Logic — Stories

| Story | Responsibility in this Unit |
|---|---|
| US-1 | Backend accepts and persists `reminder_at` in todo create/update |
| US-3 | `check_user()` detects todos with reminder_at <= now |
| US-4 | `check_user()` detects todos with due_date < today |

**Acceptance Criteria owned by Unit 2**:
- Todo model includes `reminder_at: datetime | None`
- TodoCreate and TodoUpdate accept `reminder_at`
- TodoService validates `reminder_at` format (ISO 8601 datetime)
- `check_user()` correctly identifies due reminders
- `check_user()` correctly identifies overdue todos
- `check_user()` respects deduplication (skips if notification exists)
- `check_user()` skips completed todos (status = done)
- Existing todo endpoints return `reminder_at` in responses

---

## Unit 3: Notification Bell UI — Stories

| Story | Responsibility in this Unit |
|---|---|
| US-5 | Bell icon with unread count badge |
| US-6 | Dropdown panel with notification list |
| US-7 | Mark individual notification as read (UI + API call) |
| US-8 | Mark all as read button (UI + API call) |
| US-9 | Clear all button (UI + API call) |
| US-10 | 30-second polling via useNotifications composable |

**Acceptance Criteria owned by Unit 3**:
- Bell icon visible in navbar
- Badge shows unread count (hidden when 0)
- Panel opens on bell click, closes on outside click / Escape
- Notifications display type icon, message, relative time
- Read/unread visual distinction
- Mark as read updates UI optimistically
- Mark all as read clears badge
- Clear all empties panel
- Polling starts on mount, stops on unmount
- Accessible (aria-labels, keyboard navigation)

---

## Unit 4: Reminder Form Integration — Stories

| Story | Responsibility in this Unit |
|---|---|
| US-1 | Datetime-local input in TodoForm for reminder_at |
| US-2 | Display reminder time on TodoItem + ReminderBadge |

**Acceptance Criteria owned by Unit 4**:
- TodoForm has optional datetime-local input for reminder
- Reminder can be set during create and edit
- Reminder can be cleared (set to null)
- TodoItem shows formatted reminder_at when set
- ReminderBadge shows "upcoming" (future) or "due" (past, not done)
- No badge when reminder_at is null
- Form submits reminder_at in correct ISO 8601 format
- Todo TypeScript interface includes `reminder_at: string | null`

---

## Coverage Verification

All 10 user stories are assigned to at least one unit:
- [x] US-1 → Unit 4 + Unit 2
- [x] US-2 → Unit 4
- [x] US-3 → Unit 2 + Unit 1
- [x] US-4 → Unit 2 + Unit 1
- [x] US-5 → Unit 3 + Unit 1
- [x] US-6 → Unit 3 + Unit 1
- [x] US-7 → Unit 3 + Unit 1
- [x] US-8 → Unit 3 + Unit 1
- [x] US-9 → Unit 3 + Unit 1
- [x] US-10 → Unit 3 + Unit 1

All acceptance criteria from stories.md are traceable to a specific unit's responsibility.
