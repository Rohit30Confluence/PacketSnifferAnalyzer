"""Scapy-based live packet capture adapter.

This adapter implements CapturePort using Scapy's sniff() function.
Capture runs in a dedicated thread and feeds packets into a thread-safe
ring buffer. The ring buffer is consumed by the dissection worker pool.

Privilege requirements:
    Linux:   CAP_NET_RAW + CAP_NET_ADMIN (or root)
    macOS:   root
    Windows: Administrator + Npcap installed
"""

from __future__ import annotations

from packetanalyzer.ports.capture_port import CapturePort, InterfaceInfo, PacketCallback
from packetanalyzer.domain.session import CaptureSession
from packetanalyzer.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ScapyCaptureAdapter(CapturePort):
    """Live packet capture adapter using Scapy.

    This is a scaffold. The full implementation will be added in
    Milestone 1 (Epic 2, Issue 2.3).
    """

    def list_interfaces(self) -> list[InterfaceInfo]:
        """Return all available network interfaces detected by Scapy."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def start(self, session: CaptureSession, packet_callback: PacketCallback) -> None:
        """Start live packet capture."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def stop(self) -> None:
        """Stop the capture and flush the ring buffer."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def pause(self) -> None:
        """Pause packet capture."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def resume(self) -> None:
        """Resume a paused capture."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def get_drop_count(self) -> int:
        """Return the number of dropped packets."""
        raise NotImplementedError("Implemented in Phase 3 — M1")
