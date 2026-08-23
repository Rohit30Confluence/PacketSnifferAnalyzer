"""Application-level coordinator for capture-session lifecycle."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.session import CaptureSession
    from packetanalyzer.infrastructure.audit import AuditLogger
    from packetanalyzer.ports.capture_port import CapturePort, PacketCallback
    from packetanalyzer.ports.storage_port import StoragePort

from packetanalyzer.domain.session import SessionState


class CaptureSessionManager:
    """Own exactly one active capture session at a time.

    This class is deliberately small and stateful. It is the application
    boundary between CLI/UI code and the capture/storage infrastructure.
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
        self._active_session: "CaptureSession | None" = None

    @property
    def active_session(self) -> "CaptureSession | None":
        """Return the currently active session, if any."""
        return self._active_session

    def start(
        self,
        session: "CaptureSession",
        packet_callback: "PacketCallback",
    ) -> "CaptureSession":
        """Start a new capture session atomically from the application's view."""
        if self._active_session is not None:
            raise RuntimeError(
                f"Capture session '{self._active_session.session_id}' is already active"
            )

        if session.state not in (
            SessionState.CREATED,
            SessionState.ERROR,
        ):
            raise RuntimeError(
                f"Session '{session.session_id}' cannot start from state "
                f"{session.state.name}"
            )

        try:
            self._storage.open_session(session)
            self._capture.start(session, packet_callback)
        except Exception:
            session.state = SessionState.ERROR
            self._active_session = None
            raise

        session.state = SessionState.RUNNING
        if session.started_at is None:
            session.started_at = datetime.now(timezone.utc)

        self._active_session = session
        self._audit.log_session_start(session)
        return session

    def stop(self) -> "CaptureSession":
        """Stop the active capture and close its storage."""
        session = self._require_active()

        try:
            self._capture.stop()
        finally:
            session.state = SessionState.STOPPED
            session.stopped_at = datetime.now(timezone.utc)
            session.drop_count = self._capture.get_drop_count()

            try:
                self._storage.close_session(session)
            finally:
                self._active_session = None

        self._audit.log_session_stop(session)
        return session

    def pause(self) -> "CaptureSession":
        """Pause the active capture."""
        session = self._require_active()

        if session.state != SessionState.RUNNING:
            raise RuntimeError(
                f"Capture cannot be paused from state {session.state.name}"
            )

        self._capture.pause()
        session.state = SessionState.PAUSED
        session.drop_count = self._capture.get_drop_count()
        return session

    def resume(self) -> "CaptureSession":
        """Resume a paused capture."""
        session = self._require_active()

        if session.state != SessionState.PAUSED:
            raise RuntimeError(
                f"Capture cannot be resumed from state {session.state.name}"
            )

        self._capture.resume()
        session.state = SessionState.RUNNING
        session.drop_count = self._capture.get_drop_count()
        return session

    def status(self) -> "CaptureSession | None":
        """Return the active capture session."""
        return self._active_session

    def refresh_statistics(self) -> None:
        """Refresh backend statistics on the active session."""
        session = self._active_session
        if session is None:
            return

        session.drop_count = self._capture.get_drop_count()

    def _require_active(self) -> "CaptureSession":
        session = self._active_session
        if session is None:
            raise RuntimeError("No active capture session")
        return session
