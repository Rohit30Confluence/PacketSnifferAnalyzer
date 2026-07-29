"""Abstract notification port interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.alert import AlertEvent


class NotificationPort(ABC):
    """Abstract interface for alert notification backends."""

    @abstractmethod
    def send(self, event: "AlertEvent") -> None:
        """Send an alert notification.

        Args:
            event: The alert event to notify about.

        Raises:
            NotificationError: If the notification could not be delivered.
        """

    @abstractmethod
    def is_available(self) -> bool:
        """Return True if this notification channel is currently available.

        Returns:
            True if the channel can accept notifications.
        """
