"""StatisticsSnapshot domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TopTalker:
    """A single entry in the top-talkers list.

    Attributes:
        ip_address: The IP address of the talker.
        packet_count: Total packets sent or received.
        byte_count: Total bytes sent or received.
        direction: 'src', 'dst', or 'both'.
    """

    ip_address: str
    packet_count: int
    byte_count: int
    direction: str


@dataclass(frozen=True)
class ProtocolStat:
    """Statistics for a single protocol.

    Attributes:
        protocol: The protocol name.
        packet_count: Total packets for this protocol.
        byte_count: Total bytes for this protocol.
        percentage: Percentage of total traffic (by packet count).
    """

    protocol: str
    packet_count: int
    byte_count: int
    percentage: float


@dataclass(frozen=True)
class StatisticsSnapshot:
    """A point-in-time snapshot of capture statistics.

    Attributes:
        snapshot_at: When this snapshot was taken (UTC).
        session_id: The session this snapshot belongs to.
        total_packets: Total packets captured since session start.
        total_bytes: Total bytes captured since session start.
        packets_per_second: Current packets per second rate.
        bytes_per_second: Current bytes per second rate.
        dropped_packets: Total packets dropped due to buffer overflow.
        top_talkers: Top N IP addresses by traffic volume.
        protocol_distribution: Per-protocol statistics.
        packet_size_histogram: Packet size distribution buckets.
        active_flows: Number of currently active flows.
    """

    snapshot_at: datetime
    session_id: str
    total_packets: int
    total_bytes: int
    packets_per_second: float
    bytes_per_second: float
    dropped_packets: int
    top_talkers: tuple[TopTalker, ...]
    protocol_distribution: tuple[ProtocolStat, ...]
    packet_size_histogram: dict[str, int] = field(default_factory=dict)
    active_flows: int = 0
