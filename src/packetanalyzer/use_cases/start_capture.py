"""StartCapture use case.

Orchestrates the initialization and start of a packet capture session.

The use case treats startup as a small transaction:

    storage.open_session()
        -> capture.start()
            -> audit.log_session_start()

If a later startup step fails, previously acquired resources are rolled
back best-effort before the original exception is re-raised.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.session import CaptureSession
    from packetanalyzer.ports.capture_port import CapturePort, PacketCallback
    from packetanalyzer.ports.storage_port import StoragePort
    from packetanalyzer.infrastructure.audit import AuditLogger


class StartCaptureUseCase:
    """Orchestrate starting a new packet capture session."""

    def __init__(
        self,
        capture_port: "CapturePort",
        storage_port: "StoragePort",
        audit_logger: "AuditLogger",
    ) -> None:
        self._capture = capture_port
        self._storage = storage_port
        self._audit = audit_logger

    def execute(
        self,
        session: "CaptureSession",
        packet_callback: "PacketCallback",
    ) -> None:
        """Start a capture session atomically.

        Startup order is:

        1. Open storage.
        2. Start the capture backend.
        3. Record the audit event.

        If capture startup fails, the opened storage context is closed.

        If audit logging fails after capture has started, the capture is
        stopped and storage is closed.

        The original exception is always re-raised. Cleanup failures are
        intentionally suppressed so they do not hide the root cause.
        """
        storage_opened = False
        capture_started = False

        try:
            self._storage.open_session(session)
            storage_opened = True

            self._capture.start(session, packet_callback)
            capture_started = True

            self._audit.log_session_start(session)

        except Exception:
            if capture_started:
                self._safe_stop_capture()

            if storage_opened:
                self._safe_close_storage(session)

            raise

    def _safe_stop_capture(self) -> None:
        """Best-effort rollback of a successfully started capture."""
        try:
            self._capture.stop()
        except Exception:
            pass

    def _safe_close_storage(self, session: "CaptureSession") -> None:
        """Best-effort rollback of an opened storage context."""
        try:
            self._storage.close_session(session)
        except Exception:
            pass
