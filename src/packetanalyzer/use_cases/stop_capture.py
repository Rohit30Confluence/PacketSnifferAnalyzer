"""StopCapture use case.

Stops an active capture, closes its storage, and records the final
audit event only after shutdown has completed successfully.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.session import CaptureSession
    from packetanalyzer.ports.capture_port import CapturePort
    from packetanalyzer.ports.storage_port import StoragePort
    from packetanalyzer.infrastructure.audit import AuditLogger


class StopCaptureUseCase:
    """Orchestrate stopping an active packet capture session."""

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
        """Stop a capture session.

        Shutdown order is deliberately strict:

        1. Stop the capture backend.
        2. Flush and close storage.
        3. Write the final audit event.

        If either shutdown step fails, the exception is propagated and the
        final audit event is not written because the session has not been
        confirmed as fully closed.
        """
        self._capture.stop()
        self._storage.close_session(session)
        self._audit.log_session_stop(session)
