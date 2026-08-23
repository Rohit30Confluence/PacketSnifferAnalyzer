"""CaptureSession domain model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto


class SessionState(Enum):
    """The lifecycle state of a capture session."""

    CREATED = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()
    ERROR = auto()


@dataclass
class CaptureSession:
    """Represents a bounded packet capture session.

    A session encapsulates all metadata about a capture run, including
    the interface, filter, timing, and packet statistics. It does not
    hold packet data directly — packets are stored by the storage engine.

    Attributes:
        session_id: A unique identifier (UUID) for this session.
        name: A human-readable name for the session.
        interface: The network interface(s) being captured.
        bpf_filter: The BPF filter string applied at capture time.
        started_at: When the capture started (UTC).
        stopped_at: When the capture stopped (UTC), or None if running.
        state: The current lifecycle state of the session.
        packet_count: Total packets captured.
        byte_count: Total bytes captured.
        drop_count: Packets dropped due to buffer overflow.
        operator: The OS username that started the session.
        tool_version: The PacketSnifferAnalyzer version used.
        pcap_path: Path to the PCAP file for this session, if saved.
        encrypted: Whether the session file is encrypted.
    """

    session_id: str
    name: str
    interface: str
    bpf_filter: str = ""
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    stopped_at: datetime | None = None
    state: SessionState = SessionState.CREATED
    packet_count: int = 0
    byte_count: int = 0
    drop_count: int = 0
    operator: str = ""
    tool_version: str = ""
    pcap_path: str | None = None
    encrypted: bool = False

    @property
    def duration_seconds(self) -> float | None:
        """Return the session duration in seconds, or None if still running."""
        if self.stopped_at is None:
            return None
        return (self.stopped_at - self.started_at).total_seconds()

    @property
    def is_active(self) -> bool:
        """Return True if the session is currently capturing."""
        return self.state in (SessionState.RUNNING, SessionState.PAUSED)
