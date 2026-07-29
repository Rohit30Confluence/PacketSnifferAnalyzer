"""Abstract storage port interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet
    from packetanalyzer.domain.session import CaptureSession


class StoragePort(ABC):
    """Abstract interface for packet and session storage backends."""

    @abstractmethod
    def open_session(self, session: "CaptureSession") -> None:
        """Open a storage context for a new capture session.

        Args:
            session: The session to open storage for.
        """

    @abstractmethod
    def write_packet(self, packet: "Packet") -> None:
        """Write a single packet to the storage backend.

        Args:
            packet: The packet to persist.
        """

    @abstractmethod
    def close_session(self, session: "CaptureSession") -> None:
        """Flush and close the storage context for a session.

        Args:
            session: The session to close.
        """

    @abstractmethod
    def read_packets(
        self,
        session_id: str,
        offset: int = 0,
        limit: int | None = None,
    ) -> Iterator["Packet"]:
        """Read packets from a stored session.

        Args:
            session_id: The session to read from.
            offset: Number of packets to skip from the beginning.
            limit: Maximum number of packets to return. None means all.

        Yields:
            Packet instances in capture order.
        """

    @abstractmethod
    def list_sessions(self) -> list["CaptureSession"]:
        """Return all stored sessions.

        Returns:
            A list of CaptureSession metadata objects.
        """

    @abstractmethod
    def delete_session(self, session_id: str) -> None:
        """Delete a stored session and all associated data.

        Args:
            session_id: The session to delete.
        """
