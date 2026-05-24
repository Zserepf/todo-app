"""Unit tests for NotificationService."""

import json
import os
import tempfile

import pytest

from models import Notification, NotificationType
from services.notification_service import NotificationService
from store import JSONStore
from exceptions import NotFoundError


@pytest.fixture
def temp_store():
    """Create a temporary JSON store for testing."""
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([], f)
    store = JSONStore(path)
    yield store
    os.unlink(path)


@pytest.fixture
def service(temp_store):
    """Create a NotificationService with a temporary store."""
    return NotificationService(temp_store)


class TestCreate:
    """Tests for NotificationService.create()."""

    def test_create_notification_returns_notification(self, service):
        """Create returns a Notification with correct fields."""
        result = service.create(
            user_id="user-1",
            todo_id="todo-1",
            notification_type=NotificationType.REMINDER,
            message="Reminder: Buy groceries",
        )

        assert isinstance(result, Notification)
        assert result.user_id == "user-1"
        assert result.todo_id == "todo-1"
        assert result.type == NotificationType.REMINDER
        assert result.message == "Reminder: Buy groceries"
        assert result.is_read is False
        assert result.id is not None
        assert result.created_at is not None

    def test_create_notification_persists_to_store(self, service, temp_store):
        """Create persists the notification to the JSON store."""
        service.create(
            user_id="user-1",
            todo_id="todo-1",
            notification_type=NotificationType.OVERDUE,
            message="Overdue: Submit report",
        )

        records = temp_store.read_all()
        assert len(records) == 1
        assert records[0]["user_id"] == "user-1"
        assert records[0]["todo_id"] == "todo-1"
        assert records[0]["type"] == "overdue"

    def test_create_multiple_notifications(self, service, temp_store):
        """Multiple creates add multiple records."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-1", "todo-2", NotificationType.OVERDUE, "msg2")

        records = temp_store.read_all()
        assert len(records) == 2


class TestExists:
    """Tests for NotificationService.exists()."""

    def test_exists_returns_true_when_found(self, service):
        """exists() returns True when matching notification exists."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg")

        assert service.exists("user-1", "todo-1", NotificationType.REMINDER) is True

    def test_exists_returns_false_when_not_found(self, service):
        """exists() returns False when no matching notification exists."""
        assert service.exists("user-1", "todo-1", NotificationType.REMINDER) is False

    def test_exists_differentiates_by_type(self, service):
        """exists() distinguishes between notification types."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg")

        assert service.exists("user-1", "todo-1", NotificationType.REMINDER) is True
        assert service.exists("user-1", "todo-1", NotificationType.OVERDUE) is False

    def test_exists_differentiates_by_user(self, service):
        """exists() scopes to user_id."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg")

        assert service.exists("user-1", "todo-1", NotificationType.REMINDER) is True
        assert service.exists("user-2", "todo-1", NotificationType.REMINDER) is False

    def test_exists_differentiates_by_todo(self, service):
        """exists() scopes to todo_id."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg")

        assert service.exists("user-1", "todo-1", NotificationType.REMINDER) is True
        assert service.exists("user-1", "todo-2", NotificationType.REMINDER) is False


class TestListForUser:
    """Tests for NotificationService.list_for_user()."""

    def test_list_returns_only_user_notifications(self, service):
        """list_for_user() returns only the specified user's notifications."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-2", "todo-2", NotificationType.OVERDUE, "msg2")
        service.create("user-1", "todo-3", NotificationType.OVERDUE, "msg3")

        results = service.list_for_user("user-1")
        assert len(results) == 2
        assert all(n.user_id == "user-1" for n in results)

    def test_list_sorted_by_created_at_descending(self, service):
        """list_for_user() returns notifications most recent first."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "first")
        service.create("user-1", "todo-2", NotificationType.OVERDUE, "second")

        results = service.list_for_user("user-1")
        assert results[0].message == "second"
        assert results[1].message == "first"

    def test_list_limited_to_20(self, service):
        """list_for_user() returns at most 20 notifications."""
        for i in range(25):
            service.create("user-1", f"todo-{i}", NotificationType.REMINDER, f"msg-{i}")

        results = service.list_for_user("user-1")
        assert len(results) == 20

    def test_list_empty_for_user_with_no_notifications(self, service):
        """list_for_user() returns empty list when user has no notifications."""
        results = service.list_for_user("user-1")
        assert results == []


class TestGetUnreadCount:
    """Tests for NotificationService.get_unread_count()."""

    def test_unread_count_counts_only_unread(self, service):
        """get_unread_count() counts only unread notifications for user."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-1", "todo-2", NotificationType.OVERDUE, "msg2")
        # Mark one as read
        notifications = service.list_for_user("user-1")
        service.mark_read("user-1", notifications[0].id)

        assert service.get_unread_count("user-1") == 1

    def test_unread_count_scoped_to_user(self, service):
        """get_unread_count() only counts the specified user's notifications."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-2", "todo-2", NotificationType.OVERDUE, "msg2")

        assert service.get_unread_count("user-1") == 1
        assert service.get_unread_count("user-2") == 1

    def test_unread_count_zero_when_none(self, service):
        """get_unread_count() returns 0 when user has no notifications."""
        assert service.get_unread_count("user-1") == 0


class TestMarkRead:
    """Tests for NotificationService.mark_read()."""

    def test_mark_read_sets_is_read_true(self, service):
        """mark_read() sets is_read to True."""
        created = service.create("user-1", "todo-1", NotificationType.REMINDER, "msg")

        result = service.mark_read("user-1", created.id)
        assert result.is_read is True

    def test_mark_read_raises_not_found_for_wrong_user(self, service):
        """mark_read() raises NotFoundError if notification belongs to another user."""
        created = service.create("user-1", "todo-1", NotificationType.REMINDER, "msg")

        with pytest.raises(NotFoundError):
            service.mark_read("user-2", created.id)

    def test_mark_read_raises_not_found_for_missing_id(self, service):
        """mark_read() raises NotFoundError if notification doesn't exist."""
        with pytest.raises(NotFoundError):
            service.mark_read("user-1", "nonexistent-id")


class TestMarkAllRead:
    """Tests for NotificationService.mark_all_read()."""

    def test_mark_all_read_marks_all_user_notifications(self, service):
        """mark_all_read() marks all user's notifications as read."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-1", "todo-2", NotificationType.OVERDUE, "msg2")

        count = service.mark_all_read("user-1")
        assert count == 2
        assert service.get_unread_count("user-1") == 0

    def test_mark_all_read_does_not_affect_other_users(self, service):
        """mark_all_read() only affects the specified user."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-2", "todo-2", NotificationType.OVERDUE, "msg2")

        service.mark_all_read("user-1")
        assert service.get_unread_count("user-2") == 1

    def test_mark_all_read_returns_zero_when_none_unread(self, service):
        """mark_all_read() returns 0 when no unread notifications exist."""
        count = service.mark_all_read("user-1")
        assert count == 0


class TestDeleteAll:
    """Tests for NotificationService.delete_all()."""

    def test_delete_all_removes_user_notifications(self, service):
        """delete_all() removes all notifications for the user."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-1", "todo-2", NotificationType.OVERDUE, "msg2")

        count = service.delete_all("user-1")
        assert count == 2
        assert service.list_for_user("user-1") == []

    def test_delete_all_does_not_affect_other_users(self, service):
        """delete_all() only removes the specified user's notifications."""
        service.create("user-1", "todo-1", NotificationType.REMINDER, "msg1")
        service.create("user-2", "todo-2", NotificationType.OVERDUE, "msg2")

        service.delete_all("user-1")
        assert len(service.list_for_user("user-2")) == 1

    def test_delete_all_returns_zero_when_none(self, service):
        """delete_all() returns 0 when user has no notifications."""
        count = service.delete_all("user-1")
        assert count == 0
