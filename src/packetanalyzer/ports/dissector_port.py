"""Abstract dissector port interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet


class DissectorPort(ABC):
    """Abstract interface for packet dissection backends.

    A dissector takes raw bytes and a session context and produces
    a structured Packet domain object with decoded protocol layers.
    """

    @abstractmethod
    def dissect(self, raw: bytes, session_id: str, packet_id: int, interface: str) -> "Packet":
        """Dissect raw packet bytes into a structured Packet.

        Args:
            raw: The raw packet bytes.
            session_id: The ID of the owning capture session.
            packet_id: The monotonic packet counter for this session.
            interface: The interface on which the packet was captured.

        Returns:
            A Packet instance. If dissection fails at any layer, the
            packet is returned with whatever layers were decoded and
            parse_error set to a description of the failure.
        """

    @abstractmethod
    def supported_protocols(self) -> list[str]:
        """Return the list of protocol names this dissector can decode.

        Returns:
            A list of protocol name strings (e.g., ['Ethernet', 'IPv4', 'TCP']).
        """
