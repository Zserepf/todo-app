"""Notification router handling CRUD operations for user notifications."""

import os

from fastapi import APIRouter, Depends

from dependencies import get_current_user
from models import (
    Notification,
    NotificationResponse,
    NotificationsListResponse,
    User,
)
from services.notification_service import NotificationService
from store import JSONStore

# Initialize notification store and service
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
notification_store = JSONStore(os.path.join(DATA_DIR, "notifications.json"))
notification_service = NotificationService(notification_store)

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("", response_model=NotificationsListResponse)
async def list_notifications(
    current_user: User = Depends(get_current_user),
) -> NotificationsListResponse:
    """Get notifications for the authenticated user.

    Returns up to 20 most recent notifications sorted by created_at descending,
    along with the total unread count.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        NotificationsListResponse with notifications list and unread_count.
    """
    notifications = notification_service.list_for_user(current_user.id)
    unread_count = notification_service.get_unread_count(current_user.id)

    notification_responses = [
        NotificationResponse(
            id=n.id,
            todo_id=n.todo_id,
            type=n.type,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at,
        )
        for n in notifications
    ]

    return NotificationsListResponse(
        notifications=notification_responses,
        unread_count=unread_count,
    )


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_user),
) -> NotificationResponse:
    """Mark a single notification as read.

    Verifies ownership before updating.

    Args:
        notification_id: The notification's ID to mark as read.
        current_user: The authenticated user (injected by dependency).

    Returns:
        The updated NotificationResponse.

    Raises:
        NotFoundError: If notification is not found or not owned by user.
    """
    notification = notification_service.mark_read(
        user_id=current_user.id,
        notification_id=notification_id,
    )

    return NotificationResponse(
        id=notification.id,
        todo_id=notification.todo_id,
        type=notification.type,
        message=notification.message,
        is_read=notification.is_read,
        created_at=notification.created_at,
    )


@router.post("/read-all")
async def mark_all_notifications_read(
    current_user: User = Depends(get_current_user),
) -> dict:
    """Mark all notifications as read for the authenticated user.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        A dict with message and count of notifications marked as read.
    """
    count = notification_service.mark_all_read(current_user.id)
    return {"message": "All notifications marked as read", "count": count}


@router.delete("")
async def delete_all_notifications(
    current_user: User = Depends(get_current_user),
) -> dict:
    """Delete all notifications for the authenticated user.

    Permanently removes all notifications for the user.

    Args:
        current_user: The authenticated user (injected by dependency).

    Returns:
        A dict with message and count of notifications deleted.
    """
    count = notification_service.delete_all(current_user.id)
    return {"message": "All notifications cleared", "count": count}
