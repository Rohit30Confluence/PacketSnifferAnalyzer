"""StopCapture use case."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.session import CaptureSession
    from packetanalyzer.ports.capture_port import CapturePort
    from packetanalyzer.ports.storage_port import StoragePort
    from packetanalyzer.infrastructure.audit import AuditLogger


class StopCaptureUseCase:
    """Orchestrates stopping an active packet capture session.

    This use case:
    1. Stops the capture backend
    2. Flushes and closes storage
    3. Updates session metadata
    4. Writes an audit log entry

    Args:
        capture_port: The capture backend adapter.
        storage_port: The storage backend adapter.
        audit_logger: The audit logger.
    """

    def __init__(
        self,
        capture_port: "CapturePort",
        storage_port: "StoragePort",
        audit_logger: "AuditLogger",
    ) -> None:
        self._capture = capture_port
        self._storage = storage_port
        self._audit = audit_logger

    def execute(self, session: "CaptureSession") -> None:
        """Stop a running capture session.

        Args:
            session: The session to stop.
        """
        self._capture.stop()
        self._storage.close_session(session)
        self._audit.log_session_stop(session)
