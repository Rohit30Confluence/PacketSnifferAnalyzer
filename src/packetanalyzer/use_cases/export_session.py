"""ExportSession use case."""

from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.ports.storage_port import StoragePort
    from packetanalyzer.infrastructure.audit import AuditLogger


class ExportFormat(Enum):
    """Supported export formats."""

    PCAP = auto()
    JSON = auto()
    CSV = auto()
    TEXT = auto()


class ExportSessionUseCase:
    """Exports a capture session to a specified format.

    Args:
        storage_port: The storage backend adapter.
        audit_logger: The audit logger.
    """

    def __init__(
        self,
        storage_port: "StoragePort",
        audit_logger: "AuditLogger",
    ) -> None:
        self._storage = storage_port
        self._audit = audit_logger

    def execute(
        self,
        session_id: str,
        output_path: str,
        fmt: ExportFormat,
        redact_payload: bool = False,
    ) -> int:
        """Export a session to the specified format.

        Args:
            session_id: The session to export.
            output_path: The file path to write the export to.
            fmt: The export format.
            redact_payload: If True, replace payload bytes with zeros.

        Returns:
            The number of packets exported.

        Raises:
            SessionNotFoundError: If the session does not exist.
            ExportError: If the export fails.
        """
        raise NotImplementedError(
            "ExportSessionUseCase.execute() will be implemented in Phase 3 (M3)."
        )
