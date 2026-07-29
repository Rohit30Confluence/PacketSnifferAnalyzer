"""PCAP file capture adapter.

This adapter implements CapturePort for offline PCAP file analysis.
It reads packets from a PCAP file and delivers them through the same
interface as the live capture adapter, enabling all analysis features
to work identically on live and recorded traffic.
"""

from __future__ import annotations

from pathlib import Path

from packetanalyzer.ports.capture_port import CapturePort, InterfaceInfo, PacketCallback
from packetanalyzer.domain.session import CaptureSession
from packetanalyzer.infrastructure.logging import get_logger

logger = get_logger(__name__)


class PcapFileAdapter(CapturePort):
    """Offline PCAP file analysis adapter.

    Reads packets from a PCAP file and delivers them through the
    standard CapturePort interface. Supports streaming for large files.

    Args:
        pcap_path: Path to the PCAP file to read.

    This is a scaffold. The full implementation will be added in
    Milestone 1 (Epic 2, Issue 2.3).
    """

    def __init__(self, pcap_path: Path) -> None:
        self._pcap_path = pcap_path

    def list_interfaces(self) -> list[InterfaceInfo]:
        """Return a synthetic interface representing the PCAP file."""
        return [
            InterfaceInfo(
                name=f"pcap:{self._pcap_path.name}",
                description=f"PCAP file: {self._pcap_path}",
                is_up=True,
                is_loopback=False,
            )
        ]

    def start(self, session: CaptureSession, packet_callback: PacketCallback) -> None:
        """Start reading packets from the PCAP file."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def stop(self) -> None:
        """Stop reading the PCAP file."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def pause(self) -> None:
        """Pause PCAP file reading."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def resume(self) -> None:
        """Resume PCAP file reading."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def get_drop_count(self) -> int:
        """PCAP files do not drop packets; always returns 0."""
        return 0
