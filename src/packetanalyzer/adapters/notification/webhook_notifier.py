"""HTTPS webhook notification adapter.

Security requirements:
  - Only HTTPS URLs are accepted (SR-05)
  - Webhook URL is validated before use
  - No packet payload data is included in webhook payloads
  - Timeout is enforced to prevent blocking the alert engine
"""

from __future__ import annotations

from packetanalyzer.ports.notification_port import NotificationPort
from packetanalyzer.domain.alert import AlertEvent
from packetanalyzer.infrastructure.logging import get_logger

logger = get_logger(__name__)


class WebhookNotifier(NotificationPort):
    """Sends alert notifications to an HTTPS webhook endpoint.

    Args:
        webhook_url: The HTTPS URL to POST alert events to.
        timeout_seconds: Request timeout in seconds.

    Raises:
        ValueError: If the webhook URL does not use HTTPS.
    """

    def __init__(self, webhook_url: str, timeout_seconds: int = 5) -> None:
        if not webhook_url.startswith("https://"):
            raise ValueError(
                f"Webhook URL must use HTTPS. Got: {webhook_url!r}. "
                "HTTP webhooks are not supported for security reasons."
            )
        self._webhook_url = webhook_url
        self._timeout_seconds = timeout_seconds

    def send(self, event: AlertEvent) -> None:
        """POST an alert event to the webhook URL."""
        raise NotImplementedError("Implemented in Phase 3 — M6")

    def is_available(self) -> bool:
        """Return True if the webhook URL is reachable."""
        raise NotImplementedError("Implemented in Phase 3 — M6")
