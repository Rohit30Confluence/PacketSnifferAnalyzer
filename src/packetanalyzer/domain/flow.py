"""Flow and FlowTable domain models.

A flow represents a bidirectional network conversation identified by
the standard 5-tuple: source IP, destination IP, source port,
destination port, and protocol.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto


class FlowState(Enum):
    """The state of a network flow."""

    ACTIVE = auto()
    CLOSED = auto()
    EXPIRED = auto()


@dataclass
class Flow:
    """A bidirectional network flow identified by a 5-tuple.

    Attributes:
        flow_id: A unique identifier for this flow.
        src_ip: Source IP address.
        dst_ip: Destination IP address.
        src_port: Source port number (0 for non-TCP/UDP protocols).
        dst_port: Destination port number (0 for non-TCP/UDP protocols).
        protocol: Transport protocol name (e.g., 'TCP', 'UDP', 'ICMP').
        first_seen: Timestamp of the first packet in this flow.
        last_seen: Timestamp of the most recent packet in this flow.
        packet_count: Total packets in this flow (both directions).
        byte_count: Total bytes in this flow (both directions).
        state: Current state of the flow.
    """

    flow_id: str
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    first_seen: datetime
    last_seen: datetime
    packet_count: int = 0
    byte_count: int = 0
    state: FlowState = FlowState.ACTIVE

    @property
    def five_tuple(self) -> tuple[str, str, int, int, str]:
        """Return the canonical 5-tuple for this flow."""
        return (self.src_ip, self.dst_ip, self.src_port, self.dst_port, self.protocol)

    @property
    def duration_seconds(self) -> float:
        """Return the flow duration in seconds."""
        return (self.last_seen - self.first_seen).total_seconds()

    @property
    def bytes_per_second(self) -> float:
        """Return the average throughput in bytes per second."""
        duration = self.duration_seconds
        if duration <= 0:
            return float(self.byte_count)
        return self.byte_count / duration
