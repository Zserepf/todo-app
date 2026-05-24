"""Notification service handling CRUD operations scoped to authenticated users."""

import uuid
from datetime import datetime, timezone

from exceptions import NotFoundError
from models import Notification, NotificationType
from store import JSONStore


class NotificationService:
    """Handles CRUD operations on notifications scoped to the authenticated user."""

    def __init__(self, notification_store: JSONStore):
        """Initialize with notification store.

        Args:
            notification_store: JSONStore instance for notification persistence.
        """
        self.notification_store = notification_store

    def create(
        self,
        user_id: str,
        todo_id: str,
        notification_type: NotificationType,
        message: str,
    ) -> Notification:
        """Create a notification for the user.

        Generates UUID, sets created_at, defaults is_read to False,
        and persists to store.

        Args:
            user_id: The user's ID who owns this notification.
            todo_id: The related todo's ID.
            notification_type: The type of notification (reminder or overdue).
            message: The notification message text.

        Returns:
            The created Notification object.
        """
        notification_data = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "todo_id": todo_id,
            "type": notification_type.value,
            "message": message,
            "is_read": False,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        self.notification_store.add(notification_data)

        return Notification(**notification_data)

    def exists(
        self,
        user_id: str,
        todo_id: str,
        notification_type: NotificationType,
    ) -> bool:
        """Check if a notification already exists for a given todo and type.

        Used for deduplication — only one notification per (todo_id, type)
        combination should exist per user.

        Args:
            user_id: The user's ID.
            todo_id: The related todo's ID.
            notification_type: The type of notification to check.

        Returns:
            True if a matching notification exists, False otherwise.
        """
        all_records = self.notification_store.read_all()
        for record in all_records:
            if (
                record.get("user_id") == user_id
                and record.get("todo_id") == todo_id
                and record.get("type") == notification_type.value
            ):
                return True
        return False

    def list_for_user(self, user_id: str) -> list[Notification]:
        """List notifications for a user, most recent first, limited to 20.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            A list of up to 20 Notification objects sorted by created_at descending.
        """
        all_records = self.notification_store.read_all()
        user_notifications = [r for r in all_records if r.get("user_id") == user_id]

        # Sort by created_at descending (most recent first)
        user_notifications.sort(key=lambda r: r.get("created_at", ""), reverse=True)

        # Limit to 20
        user_notifications = user_notifications[:20]

        return [Notification(**r) for r in user_notifications]

    def get_unread_count(self, user_id: str) -> int:
        """Count unread notifications for a user.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            The number of unread notifications.
        """
        all_records = self.notification_store.read_all()
        return sum(
            1
            for r in all_records
            if r.get("user_id") == user_id and not r.get("is_read", False)
        )

    def mark_read(self, user_id: str, notification_id: str) -> Notification:
        """Mark a single notification as read.

        Verifies ownership before updating.

        Args:
            user_id: The authenticated user's ID.
            notification_id: The notification's ID to mark as read.

        Returns:
            The updated Notification object.

        Raises:
            NotFoundError: If notification is not found or not owned by user.
        """
        record = self.notification_store.find_by_id(notification_id)

        if not record or record.get("user_id") != user_id:
            raise NotFoundError("Notification not found")

        updated_record = self.notification_store.update(notification_id, {"is_read": True})

        if not updated_record:
            raise NotFoundError("Notification not found")

        return Notification(**updated_record)

    def mark_all_read(self, user_id: str) -> int:
        """Mark all notifications as read for a user.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            The number of notifications marked as read.
        """
        all_records = self.notification_store.read_all()
        count = 0

        for record in all_records:
            if record.get("user_id") == user_id and not record.get("is_read", False):
                record["is_read"] = True
                count += 1

        if count > 0:
            self.notification_store.write_all(all_records)

        return count

    def delete_all(self, user_id: str) -> int:
        """Delete all notifications for a user.

        Args:
            user_id: The authenticated user's ID.

        Returns:
            The number of notifications deleted.
        """
        all_records = self.notification_store.read_all()
        original_count = len([r for r in all_records if r.get("user_id") == user_id])

        remaining = [r for r in all_records if r.get("user_id") != user_id]

        if original_count > 0:
            self.notification_store.write_all(remaining)

        return original_count
