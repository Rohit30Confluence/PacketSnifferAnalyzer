"""Abstract capture port interface.

Defines the contract that all capture adapters must implement,
whether they capture from a live interface or read from a PCAP file.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet
    from packetanalyzer.domain.session import CaptureSession

# Type alias for the callback invoked on each captured packet.
PacketCallback = Callable[["Packet"], None]


class InterfaceInfo:
    """Metadata about a network interface.

    Attributes:
        name: The OS-level interface name (e.g., 'eth0', 'wlan0').
        description: A human-readable description.
        is_up: Whether the interface is currently up.
        is_loopback: Whether this is a loopback interface.
        addresses: List of IP addresses assigned to this interface.
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        is_up: bool = True,
        is_loopback: bool = False,
        addresses: list[str] | None = None,
    ) -> None:
        self.name = name
        self.description = description
        self.is_up = is_up
        self.is_loopback = is_loopback
        self.addresses = addresses or []


class CapturePort(ABC):
    """Abstract interface for packet capture backends.

    Implementations must be thread-safe. The capture loop runs in a
    dedicated thread and invokes the packet_callback for each captured
    packet. The callback must be non-blocking.
    """

    @abstractmethod
    def list_interfaces(self) -> list[InterfaceInfo]:
        """Return all available network interfaces on the host.

        Returns:
            A list of InterfaceInfo objects, one per interface.

        Raises:
            PrivilegeError: If insufficient privileges to enumerate interfaces.
        """

    @abstractmethod
    def start(
        self,
        session: "CaptureSession",
        packet_callback: PacketCallback,
    ) -> None:
        """Start capturing packets.

        Args:
            session: The capture session configuration.
            packet_callback: Called for each captured packet. Must be
                non-blocking; heavy processing should be deferred.

        Raises:
            PrivilegeError: If insufficient privileges for raw capture.
            InterfaceNotFoundError: If the specified interface does not exist.
            FilterSyntaxError: If the BPF filter string is invalid.
            CaptureAlreadyRunningError: If a capture is already in progress.
        """

    @abstractmethod
    def stop(self) -> None:
        """Stop the capture and flush any buffered packets.

        This method blocks until the capture thread has terminated cleanly.
        """

    @abstractmethod
    def pause(self) -> None:
        """Pause packet capture without terminating the capture thread.

        Packets arriving during a pause are discarded. The drop counter
        is NOT incremented for paused packets.
        """

    @abstractmethod
    def resume(self) -> None:
        """Resume a paused capture.

        Raises:
            CaptureNotPausedError: If the capture is not currently paused.
        """

    @abstractmethod
    def get_drop_count(self) -> int:
        """Return the number of packets dropped since capture started.

        Returns:
            The cumulative drop count reported by the capture backend.
        """
