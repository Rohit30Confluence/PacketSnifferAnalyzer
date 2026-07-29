"""StartCapture use case.

Orchestrates the initialization and start of a packet capture session.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.session import CaptureSession
    from packetanalyzer.ports.capture_port import CapturePort, PacketCallback
    from packetanalyzer.ports.storage_port import StoragePort
    from packetanalyzer.infrastructure.audit import AuditLogger


class StartCaptureUseCase:
    """Orchestrates starting a new packet capture session.

    This use case:
    1. Validates the session configuration
    2. Opens storage for the session
    3. Starts the capture backend
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

    def execute(
        self,
        session: "CaptureSession",
        packet_callback: "PacketCallback",
    ) -> None:
        """Start a capture session.

        Args:
            session: The configured capture session.
            packet_callback: Callback invoked for each captured packet.

        Raises:
            PrivilegeError: If insufficient privileges.
            InterfaceNotFoundError: If the interface does not exist.
            FilterSyntaxError: If the BPF filter is invalid.
        """
        self._storage.open_session(session)
        self._capture.start(session, packet_callback)
        self._audit.log_session_start(session)
