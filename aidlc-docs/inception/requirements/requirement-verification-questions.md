# Requirements Verification Questions

## Question 1
What notification types should the system support?

A) Reminder only (user-set reminder time)

B) Overdue only (past due_date with status != done)

C) Both reminder and overdue notifications

D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 2
How should the notification check be triggered?

A) Background scheduler (cron job, celery beat)

B) Lazy evaluation on API request (check when /api/notifications is called)

C) WebSocket push from server

D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 3
What polling interval should the frontend use?

A) 10 seconds

B) 30 seconds

C) 60 seconds

D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 4
Should notifications persist across sessions (stored server-side)?

A) Yes — stored in notifications.json, survives page refresh

B) No — in-memory only, lost on refresh

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5
How should duplicate notifications be handled (e.g., same todo triggers overdue notification every poll)?

A) Create only one notification per todo per type — never duplicate

B) Create a new notification each time the condition is detected

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 6
What is the maximum number of notifications to return in the dropdown?

A) 20 most recent

B) 50 most recent

C) All notifications (no limit)

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 7
Should clearing all notifications permanently delete them or soft-delete?

A) Permanent delete (remove from notifications.json)

B) Soft delete (mark as cleared, hide from UI)

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 8
What datetime format should reminder_at use?

A) ISO 8601 full datetime with timezone (e.g., 2026-05-21T14:30:00Z)

B) ISO 8601 datetime without timezone (e.g., 2026-05-21T14:30:00)

C) Date only (YYYY-MM-DD) — triggers at start of day

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 9
Should the "overdue" check use due_date (date only) or a specific time?

A) Due date comparison — overdue if due_date < today AND status != done

B) Due date + time comparison

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 10
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints

B) No — skip all SECURITY rules (suitable for PoCs, prototypes)

C) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 11
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints

B) Partial — enforce PBT rules only for pure functions and serialization round-trips

C) No — skip all PBT rules (suitable for simple CRUD applications)

D) Other (please describe after [Answer]: tag below)

[Answer]: C
