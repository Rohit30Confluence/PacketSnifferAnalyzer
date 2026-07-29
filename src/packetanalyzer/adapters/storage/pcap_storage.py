"""PCAP file storage adapter.

Implements StoragePort using the PCAP file format. Supports:
  - Streaming writes (no full-file buffering)
  - Streaming reads (chunk-based for large files)
  - File rotation by size and time
  - Corrupt file recovery (reads valid packets up to corruption point)
  - Optional AES-256-GCM encryption
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from packetanalyzer.ports.storage_port import StoragePort
from packetanalyzer.domain.packet import Packet
from packetanalyzer.domain.session import CaptureSession
from packetanalyzer.infrastructure.logging import get_logger

logger = get_logger(__name__)


class PcapStorageAdapter(StoragePort):
    """PCAP file storage adapter.

    Args:
        data_dir: Directory for storing PCAP files and session metadata.
        rotation_size_mb: Rotate PCAP files when they reach this size.
        rotation_interval_hours: Rotate PCAP files at this time interval.

    This is a scaffold. The full implementation will be added in
    Milestone 3 (Epic 4, Issue 4.1).
    """

    def __init__(
        self,
        data_dir: Path,
        rotation_size_mb: int = 100,
        rotation_interval_hours: int = 1,
    ) -> None:
        self._data_dir = data_dir
        self._rotation_size_mb = rotation_size_mb
        self._rotation_interval_hours = rotation_interval_hours

    def open_session(self, session: CaptureSession) -> None:
        """Open a PCAP file for writing."""
        raise NotImplementedError("Implemented in Phase 3 — M3")

    def write_packet(self, packet: Packet) -> None:
        """Write a packet to the current PCAP file."""
        raise NotImplementedError("Implemented in Phase 3 — M3")

    def close_session(self, session: CaptureSession) -> None:
        """Flush and close the current PCAP file."""
        raise NotImplementedError("Implemented in Phase 3 — M3")

    def read_packets(
        self,
        session_id: str,
        offset: int = 0,
        limit: int | None = None,
    ) -> Iterator[Packet]:
        """Stream packets from a stored PCAP file."""
        raise NotImplementedError("Implemented in Phase 3 — M3")
        return  # noqa: unreachable
        yield  # Make this a generator

    def list_sessions(self) -> list[CaptureSession]:
        """Return all stored sessions."""
        raise NotImplementedError("Implemented in Phase 3 — M3")

    def delete_session(self, session_id: str) -> None:
        """Delete a session and its PCAP files."""
        raise NotImplementedError("Implemented in Phase 3 — M3")
