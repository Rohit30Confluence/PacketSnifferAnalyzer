"""Packet and Layer domain models.

These are the core data structures that flow through the entire system.
They are immutable value objects with no behavior beyond data representation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class Layer:
    """A single decoded protocol layer within a packet.

    Attributes:
        protocol: The protocol name (e.g., 'TCP', 'IPv4', 'DNS').
        fields: A mapping of field names to their decoded values.
        raw_bytes: The raw bytes for this layer, if available.
    """

    protocol: str
    fields: dict[str, Any] = field(default_factory=dict)
    raw_bytes: bytes = field(default=b"")

    def get_field(self, name: str, default: Any = None) -> Any:
        """Retrieve a field value by name.

        Args:
            name: The field name to look up.
            default: Value to return if the field is not present.

        Returns:
            The field value, or default if not found.
        """
        return self.fields.get(name, default)


@dataclass(frozen=True)
class Packet:
    """A captured and dissected network packet.

    This is the central domain object. It is produced by the dissection
    engine and consumed by the filter, analysis, alert, and storage engines.

    Attributes:
        packet_id: A monotonically increasing identifier within a session.
        timestamp: The time the packet was captured (UTC).
        interface: The network interface on which the packet was captured.
        length: The total length of the packet in bytes.
        captured_length: The number of bytes actually captured (may be less
            than length if a snaplen limit was applied).
        layers: An ordered list of decoded protocol layers, from outermost
            (e.g., Ethernet) to innermost (e.g., application payload).
        raw_bytes: The complete raw packet bytes.
        session_id: The identifier of the capture session this packet
            belongs to.
        parse_error: If set, indicates that dissection failed at some layer.
            The packet is still stored with whatever layers were decoded.
    """

    packet_id: int
    timestamp: datetime
    interface: str
    length: int
    captured_length: int
    layers: tuple[Layer, ...]
    raw_bytes: bytes
    session_id: str
    parse_error: str | None = None

    @property
    def is_complete(self) -> bool:
        """Return True if the packet was fully captured (no truncation)."""
        return self.captured_length >= self.length

    @property
    def has_parse_error(self) -> bool:
        """Return True if dissection encountered an error."""
        return self.parse_error is not None

    def get_layer(self, protocol: str) -> Layer | None:
        """Return the first layer matching the given protocol name.

        Args:
            protocol: The protocol name to search for (case-insensitive).

        Returns:
            The matching Layer, or None if not present.
        """
        protocol_upper = protocol.upper()
        for layer in self.layers:
            if layer.protocol.upper() == protocol_upper:
                return layer
        return None

    def has_layer(self, protocol: str) -> bool:
        """Return True if the packet contains a layer for the given protocol.

        Args:
            protocol: The protocol name to check (case-insensitive).

        Returns:
            True if the protocol layer is present.
        """
        return self.get_layer(protocol) is not None

    def summary(self) -> str:
        """Return a one-line human-readable summary of the packet.

        Returns:
            A string in the format: 'No. | Time | Src -> Dst | Protocol | Length'
        """
        protocols = " / ".join(layer.protocol for layer in self.layers)
        return (
            f"#{self.packet_id} "
            f"{self.timestamp.isoformat()} "
            f"{protocols} "
            f"{self.length}B"
        )
