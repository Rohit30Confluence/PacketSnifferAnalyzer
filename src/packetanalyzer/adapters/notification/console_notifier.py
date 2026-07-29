"""Console notification adapter."""

from __future__ import annotations

from packetanalyzer.ports.notification_port import NotificationPort
from packetanalyzer.domain.alert import AlertEvent
from packetanalyzer.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ConsoleNotifier(NotificationPort):
    """Sends alert notifications to the console (stderr)."""

    def send(self, event: AlertEvent) -> None:
        """Print an alert to stderr."""
        raise NotImplementedError("Implemented in Phase 3 — M6")

    def is_available(self) -> bool:
        """Console is always available."""
        return True
