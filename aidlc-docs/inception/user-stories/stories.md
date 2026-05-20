# User Stories — Reminders & Notifications

## Epic: Reminder Management

### US-1: Set Reminder on Todo
**As** Alex (busy professional),
**I want to** set a reminder date/time on a todo,
**So that** I get notified before or when the task needs attention.

**Acceptance Criteria:**
- [ ] Todo create form has an optional datetime-local input for reminder
- [ ] Todo edit form shows and allows editing the reminder datetime
- [ ] Reminder can be cleared (set to null)
- [ ] Backend accepts `reminder_at` as ISO 8601 datetime in create/update endpoints
- [ ] Backend returns `reminder_at` in todo responses

### US-2: View Reminder on Todo Card
**As** Alex,
**I want to** see the reminder time displayed on my todo cards,
**So that** I know which todos have reminders set.

**Acceptance Criteria:**
- [ ] Todo card shows reminder datetime when `reminder_at` is set
- [ ] A visual badge indicates reminder status: "upcoming" or "due"
- [ ] Badge shows "upcoming" when reminder_at is in the future
- [ ] Badge shows "due" (warning style) when reminder_at has passed and todo is not done
- [ ] No badge shown when reminder_at is null

---

## Epic: Notification Generation

### US-3: Generate Reminder Notifications
**As** Alex,
**I want** the system to create a notification when my reminder time arrives,
**So that** I'm alerted to take action on the todo.

**Acceptance Criteria:**
- [ ] When GET /api/notifications is called, system checks for todos where reminder_at <= now AND status != done
- [ ] A notification of type 'reminder' is created for each qualifying todo
- [ ] Notification message includes the todo title (e.g., "Reminder: Buy groceries")
- [ ] Only one reminder notification per todo is ever created (deduplication)
- [ ] Completed todos (status = done) never generate reminder notifications

### US-4: Generate Overdue Notifications
**As** Alex,
**I want** the system to notify me when a todo becomes overdue,
**So that** I can prioritize catching up on missed deadlines.

**Acceptance Criteria:**
- [ ] When GET /api/notifications is called, system checks for todos where due_date < today AND status != done
- [ ] A notification of type 'overdue' is created for each qualifying todo
- [ ] Notification message includes the todo title (e.g., "Overdue: Submit report")
- [ ] Only one overdue notification per todo is ever created (deduplication)
- [ ] Completed todos never generate overdue notifications

---

## Epic: Notification Viewing & Management

### US-5: View Notifications via Bell Icon
**As** Alex,
**I want to** see a notification bell in the navbar with an unread count,
**So that** I know at a glance if I have pending notifications.

**Acceptance Criteria:**
- [ ] Bell icon is visible in the dashboard header/navbar
- [ ] Unread count badge appears on the bell when unread_count > 0
- [ ] Badge is hidden when unread_count is 0
- [ ] Badge shows the numeric count (e.g., "3")
- [ ] Bell icon is accessible (aria-label, keyboard navigable)

### US-6: View Notification Panel
**As** Alex,
**I want to** click the bell to see my recent notifications,
**So that** I can review what needs my attention.

**Acceptance Criteria:**
- [ ] Clicking the bell opens a dropdown panel
- [ ] Panel shows up to 20 most recent notifications
- [ ] Each notification displays: type icon (bell/clock), message, relative time ("2 min ago")
- [ ] Unread notifications are visually distinct from read ones
- [ ] Panel closes when clicking outside or pressing Escape
- [ ] Panel is accessible (focus trap, aria attributes)

### US-7: Mark Notification as Read
**As** Alex,
**I want to** mark individual notifications as read,
**So that** I can track which ones I've already seen.

**Acceptance Criteria:**
- [ ] Clicking a notification or its "mark read" button marks it as read
- [ ] The notification visually changes to "read" state
- [ ] Unread count badge decreases by 1
- [ ] Backend persists the is_read=true state

### US-8: Mark All Notifications as Read
**As** Sam (team lead with many notifications),
**I want to** mark all notifications as read at once,
**So that** I can quickly clear my notification backlog.

**Acceptance Criteria:**
- [ ] "Mark all as read" button is visible in the notification panel
- [ ] Clicking it marks all user's notifications as is_read=true
- [ ] Unread count badge resets to 0 (hidden)
- [ ] All notifications in the panel update to "read" visual state

### US-9: Clear All Notifications
**As** Sam,
**I want to** clear all my notifications permanently,
**So that** I can start fresh without old notification clutter.

**Acceptance Criteria:**
- [ ] "Clear all" button is visible in the notification panel
- [ ] Clicking it permanently deletes all user's notifications
- [ ] Panel shows empty state after clearing
- [ ] Unread count badge is hidden
- [ ] Confirmation is shown before clearing (optional UX enhancement)

---

## Epic: Polling & Real-time Updates

### US-10: Automatic Notification Polling
**As** Alex,
**I want** the app to automatically check for new notifications,
**So that** I see updates without manually refreshing.

**Acceptance Criteria:**
- [ ] Frontend polls GET /api/notifications every 30 seconds
- [ ] First poll happens immediately on dashboard mount
- [ ] Polling stops when user logs out
- [ ] Polling stops when user navigates away from dashboard
- [ ] New notifications appear in the panel without page refresh
- [ ] Unread count updates automatically

---

## Story Summary

| ID | Story | Unit |
|---|---|---|
| US-1 | Set Reminder on Todo | Unit 4 (Reminder Form) + Unit 2 (Backend) |
| US-2 | View Reminder on Todo Card | Unit 4 (Reminder Form) |
| US-3 | Generate Reminder Notifications | Unit 2 (Reminder Trigger) |
| US-4 | Generate Overdue Notifications | Unit 2 (Reminder Trigger) |
| US-5 | View Notifications via Bell Icon | Unit 3 (Bell UI) |
| US-6 | View Notification Panel | Unit 3 (Bell UI) |
| US-7 | Mark Notification as Read | Unit 1 (Backend) + Unit 3 (Bell UI) |
| US-8 | Mark All as Read | Unit 1 (Backend) + Unit 3 (Bell UI) |
| US-9 | Clear All Notifications | Unit 1 (Backend) + Unit 3 (Bell UI) |
| US-10 | Automatic Polling | Unit 3 (Bell UI) |
