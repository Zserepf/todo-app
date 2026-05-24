# Unit Test Execution — Unit 1: Notification Backend

## Run Unit Tests

### 1. Execute All Unit Tests
```bash
cd backend
python -m pytest tests/test_notification_service.py -v
```

### 2. Expected Results
- **Total Tests**: 24
- **Expected**: 24 passed, 0 failures
- **Test Classes**:
  - `TestCreate` (3 tests) — notification creation and persistence
  - `TestExists` (5 tests) — deduplication check by user/todo/type
  - `TestListForUser` (4 tests) — user scoping, sort order, limit
  - `TestGetUnreadCount` (3 tests) — unread counting and scoping
  - `TestMarkRead` (3 tests) — mark read + ownership verification
  - `TestMarkAllRead` (3 tests) — bulk mark read + user isolation
  - `TestDeleteAll` (3 tests) — bulk delete + user isolation

### 3. Run with Coverage (Optional)
```bash
pip install pytest-cov
python -m pytest tests/test_notification_service.py -v --cov=services.notification_service --cov-report=term-missing
```

### 4. Fix Failing Tests
If tests fail:
1. Review test output for assertion errors
2. Check that `backend/models.py` has NotificationType and Notification models
3. Check that `backend/services/notification_service.py` exists and imports correctly
4. Verify `backend/exceptions.py` has NotFoundError class
5. Rerun tests until all pass
