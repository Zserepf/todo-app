# Component Dependencies

## Dependency Matrix

| Component | Depends On | Communication Pattern |
|---|---|---|
| NotificationRouter | NotificationService, ReminderChecker, TodoStore, get_current_user | Direct function call |
| NotificationService | JSONStore (notification_store) | Direct function call |
| ReminderChecker | (none — pure function) | Receives data as params |
| TodoService (extended) | JSONStore (todo_store) | Direct function call (existing) |
| NotificationBell.vue | useNotifications composable | Reactive state binding |
| NotificationPanel.vue | useNotifications composable | Reactive state + actions |
| useNotifications.ts | notificationsApi (utils/api.ts) | HTTP fetch calls |
| ReminderBadge.vue | (none — receives props) | Props from parent |
| TodoForm.vue (extended) | (existing deps + reminder_at field) | Emits form data |
| TodoItem.vue (extended) | ReminderBadge component | Component composition |

---

## Cross-Unit Dependencies

```
Unit 4 (Reminder Form UI)
    |
    | depends on Unit 2's API contract
    | (Todo model includes reminder_at field)
    v
Unit 2 (Reminder Trigger Logic)
    |
    | depends on Unit 1's service
    | (calls notification_service.create to generate notifications)
    v
Unit 1 (Notification Backend)
    |
    | no upstream dependencies
    | (standalone CRUD service)

Unit 3 (Notification Bell UI)
    |
    | depends on Unit 1's API contract
    | (calls GET/PATCH/POST/DELETE /api/notifications)
    v
Unit 1 (Notification Backend)
```

---

## Data Flow Diagram

```
+------------------+       +---------------------+       +-------------------+
|  TodoForm.vue    | ----> | PUT/POST /api/todos | ----> | TodoService       |
| (reminder_at)    |       | (with reminder_at)  |       | (persist to JSON) |
+------------------+       +---------------------+       +-------------------+

+------------------+       +------------------------+       +------------------+
| NotificationBell | ----> | GET /api/notifications | ----> | NotificationRouter|
| (polls every 30s)|       |                        |       |                  |
+------------------+       +------------------------+       +------------------+
                                                                    |
                                                    +---------------+---------------+
                                                    |                               |
                                                    v                               v
                                          +------------------+           +-------------------+
                                          | ReminderChecker  |           | NotificationService|
                                          | (detect due)     |           | (create + list)    |
                                          +------------------+           +-------------------+
```

---

## Integration Points

### Backend Internal
- `NotificationRouter` imports `NotificationService`, `ReminderChecker`, `todo_store`
- `NotificationRouter` uses `get_current_user` dependency (existing)
- `main.py` registers new `notifications_router`

### Frontend Internal
- `dashboard.vue` imports `NotificationBell` component
- `NotificationBell` imports `NotificationPanel` component
- `NotificationBell` uses `useNotifications` composable
- `TodoForm.vue` adds `reminder_at` to form data
- `TodoItem.vue` imports `ReminderBadge` component
- `utils/api.ts` exports new `notificationsApi` object
- `types/index.ts` exports new `Notification` interface
