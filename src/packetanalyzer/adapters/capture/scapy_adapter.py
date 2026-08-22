"""Scapy-based live packet capture adapter."""

from __future__ import annotations

from scapy.all import conf
from scapy.interfaces import NetworkInterface

from packetanalyzer.domain.session import CaptureSession
from packetanalyzer.infrastructure.logging import get_logger
from packetanalyzer.ports.capture_port import (
    CapturePort,
    InterfaceInfo,
    PacketCallback,
)

logger = get_logger(__name__)


class ScapyCaptureAdapter(CapturePort):
    """Live packet capture adapter using Scapy."""

    def list_interfaces(self) -> list[InterfaceInfo]:
        """Return all available network interfaces detected by Scapy."""
        interfaces: list[InterfaceInfo] = []

        for raw_interface in conf.ifaces.values():
            if not isinstance(raw_interface, NetworkInterface):
                continue

            addresses: list[str] = []

            for version_addresses in raw_interface.ips.values():
                for raw_address in version_addresses:
                    address = str(raw_address)

                    # Scapy reports unspecified addresses on some
                    # macOS virtual interfaces. They are not assigned
                    # interface addresses and should not enter the domain.
                    if address in {"0.0.0.0", "::"}:
                        continue

                    addresses.append(address)

            flags = raw_interface.flags

            interfaces.append(
                InterfaceInfo(
                    name=raw_interface.name,
                    description=raw_interface.description or raw_interface.name,
                    is_up=bool(flags & "UP"),
                    is_loopback=bool(flags & "LOOPBACK"),
                    addresses=addresses,
                )
            )

        return interfaces

    def start(
        self,
        session: CaptureSession,
        packet_callback: PacketCallback,
    ) -> None:
        """Start live packet capture."""
        raise NotImplementedError("Live capture is implemented in M2.")

    def stop(self) -> None:
        """Stop the capture."""
        raise NotImplementedError("Live capture is implemented in M2.")

    def pause(self) -> None:
        """Pause packet capture."""
        raise NotImplementedError("Live capture is implemented in M2.")

    def resume(self) -> None:
        """Resume a paused capture."""
        raise NotImplementedError("Live capture is implemented in M2.")

    def get_drop_count(self) -> int:
        """Return the number of dropped packets."""
        raise NotImplementedError("Live capture is implemented in M2.")
