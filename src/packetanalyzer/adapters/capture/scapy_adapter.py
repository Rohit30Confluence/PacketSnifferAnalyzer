"""Scapy-based live packet capture adapter.

Capture architecture:

    Scapy sniff thread
        |
        v
    bounded packet queue
        |
        v
    processing worker
        |
        +--> domain dissection
        +--> session statistics
        +--> domain callback

The capture callback never performs domain dissection directly.
"""

from __future__ import annotations

from collections import deque
from threading import Event, Lock, Thread, current_thread
from typing import Any, Protocol

from scapy.all import conf, sniff
from scapy.interfaces import NetworkInterface

from packetanalyzer.adapters.dissection.scapy_dissector import ScapyDissector
from packetanalyzer.domain.packet import Packet
from packetanalyzer.domain.session import CaptureSession, SessionState
from packetanalyzer.infrastructure.logging import get_logger
from packetanalyzer.ports.capture_port import (
    CapturePort,
    InterfaceInfo,
    PacketCallback,
)

logger = get_logger(__name__)


class PacketDissector(Protocol):
    """Boundary used to convert raw captured bytes into domain packets."""

    def dissect(
        self,
        raw: bytes,
        session_id: str,
        packet_id: int,
        interface: str,
    ) -> Packet:
        """Dissect raw bytes into a domain Packet."""


class ScapyCaptureAdapter(CapturePort):
    """Thread-safe live capture adapter backed by Scapy."""

    _QUEUE_LIMIT = 1024
    _POLL_INTERVAL = 0.05
    _JOIN_TIMEOUT = 5.0

    def __init__(self, dissector: PacketDissector | None = None) -> None:
        self._dissector = dissector or ScapyDissector()

        self._lock = Lock()
        self._stop_event = Event()
        self._wake_event = Event()

        self._capture_worker: Thread | None = None
        self._processing_worker: Thread | None = None

        self._session: CaptureSession | None = None
        self._callback: PacketCallback | None = None

        self._queue: deque[Any] = deque()
        self._drop_count = 0
        self._next_packet_id = 0

    # ------------------------------------------------------------------
    # Interface discovery
    # ------------------------------------------------------------------

    def list_interfaces(self) -> list[InterfaceInfo]:
        """Return normalized interface information from Scapy."""
        result: list[InterfaceInfo] = []

        for raw_interface in conf.ifaces.values():
            if not isinstance(raw_interface, NetworkInterface):
                continue

            addresses: list[str] = []

            for version_addresses in raw_interface.ips.values():
                for raw_address in version_addresses:
                    address = str(raw_address)

                    if address in {"0.0.0.0", "::"}:
                        continue

                    if address not in addresses:
                        addresses.append(address)

            flags = raw_interface.flags

            result.append(
                InterfaceInfo(
                    name=raw_interface.name,
                    description=(
                        raw_interface.description
                        or raw_interface.name
                    ),
                    is_up=bool(flags & "UP"),
                    is_loopback=bool(flags & "LOOPBACK"),
                    addresses=addresses,
                )
            )

        return result

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(
        self,
        session: CaptureSession,
        packet_callback: PacketCallback,
    ) -> None:
        """Start Scapy capture and packet processing workers."""
        if not session.interface:
            raise ValueError("Capture interface is required")

        if not self._interface_exists(session.interface):
            raise ValueError(
                f"Capture interface does not exist: {session.interface}"
            )

        with self._lock:
            if self._is_running_locked():
                raise RuntimeError("Capture is already running")

            self._session = session
            self._callback = packet_callback

            self._queue.clear()
            self._drop_count = 0
            self._next_packet_id = 0

            self._stop_event.clear()
            self._wake_event.clear()

            session.packet_count = 0
            session.byte_count = 0
            session.drop_count = 0
            session.state = SessionState.RUNNING

            self._processing_worker = Thread(
                target=self._processing_loop,
                name="packetanalyzer-processing",
                daemon=True,
            )

            self._capture_worker = Thread(
                target=self._capture_loop,
                name="packetanalyzer-capture",
                daemon=True,
            )

            processing_worker = self._processing_worker
            capture_worker = self._capture_worker

            processing_worker.start()
            capture_worker.start()

    def stop(self) -> None:
        """Stop both workers and finalize the session."""
        with self._lock:
            capture_worker = self._capture_worker
            processing_worker = self._processing_worker
            session = self._session

            if capture_worker is None and processing_worker is None:
                return

            self._stop_event.set()
            self._wake_event.set()

        self._join_worker(capture_worker)
        self._join_worker(processing_worker)

        with self._lock:
            session = self._session

            if session is not None:
                session.drop_count = self._drop_count

                if session.state in (
                    SessionState.RUNNING,
                    SessionState.PAUSED,
                ):
                    session.state = SessionState.STOPPED

            self._queue.clear()

            self._capture_worker = None
            self._processing_worker = None
            self._callback = None
            self._session = None

    def pause(self) -> None:
        """Pause capture delivery without stopping Scapy."""
        with self._lock:
            if not self._is_running_locked():
                raise RuntimeError("Capture is not running")

            if self._session is None:
                raise RuntimeError("No active capture session")

            if self._session.state != SessionState.RUNNING:
                raise RuntimeError("Capture is not running")

            self._session.state = SessionState.PAUSED

    def resume(self) -> None:
        """Resume capture delivery."""
        with self._lock:
            if not self._is_running_locked():
                raise RuntimeError("Capture is not running")

            if self._session is None:
                raise RuntimeError("No active capture session")

            if self._session.state != SessionState.PAUSED:
                raise RuntimeError("Capture is not paused")

            self._session.state = SessionState.RUNNING

    def get_drop_count(self) -> int:
        """Return the cumulative capture-processing drop count."""
        with self._lock:
            return self._drop_count

    # ------------------------------------------------------------------
    # Capture worker
    # ------------------------------------------------------------------

    def _capture_loop(self) -> None:
        """Run Scapy's capture loop."""
        with self._lock:
            session = self._session

        if session is None:
            return

        try:
            sniff(
                iface=session.interface,
                filter=session.bpf_filter or None,
                prn=self._on_scapy_packet,
                store=False,
                timeout=self._POLL_INTERVAL,
                stop_filter=self._should_stop,
            )

        except Exception as exc:
            logger.exception(
                "capture_worker_failed",
                error=str(exc),
                interface=session.interface,
            )

            with self._lock:
                if self._session is session:
                    session.state = SessionState.ERROR

            self._stop_event.set()
            self._wake_event.set()

    def _on_scapy_packet(self, raw_packet: Any) -> None:
        """Accept a raw Scapy packet and enqueue it for processing."""
        with self._lock:
            if self._stop_event.is_set():
                return

            session = self._session

            if session is None:
                return

            if session.state == SessionState.PAUSED:
                return

            if session.state != SessionState.RUNNING:
                return

            if len(self._queue) >= self._QUEUE_LIMIT:
                self._record_drop_locked()
                return

            self._queue.append(raw_packet)
            self._wake_event.set()

    # ------------------------------------------------------------------
    # Processing worker
    # ------------------------------------------------------------------

    def _processing_loop(self) -> None:
        """Consume queued packets and deliver domain packets."""
        while True:
            item = self._next_queued_packet()

            if item is None:
                with self._lock:
                    should_exit = (
                        self._stop_event.is_set()
                        and not self._queue
                    )

                if should_exit:
                    return

                self._wake_event.wait(self._POLL_INTERVAL)
                self._wake_event.clear()
                continue

            self._process_packet(item)

    def _next_queued_packet(self) -> Any | None:
        """Remove and return one packet from the queue."""
        with self._lock:
            if not self._queue:
                return None

            return self._queue.popleft()

    def _process_packet(self, raw_packet: Any) -> None:
        """Dissect one packet and invoke the domain callback."""
        with self._lock:
            session = self._session
            callback = self._callback

            if session is None or callback is None:
                return

            if self._stop_event.is_set():
                return

            if session.state == SessionState.PAUSED:
                return

            self._next_packet_id += 1
            packet_id = self._next_packet_id

        try:
            raw = bytes(raw_packet)

            packet = self._dissector.dissect(
                raw=raw,
                session_id=session.session_id,
                packet_id=packet_id,
                interface=session.interface,
            )

            with self._lock:
                if self._stop_event.is_set():
                    return

                if self._session is not session:
                    return

                if session.state == SessionState.PAUSED:
                    return

                session.packet_count += 1
                session.byte_count += len(raw)

            callback(packet)

        except Exception as exc:
            with self._lock:
                self._record_drop_locked()

                if self._session is session:
                    session.drop_count = self._drop_count

            logger.exception(
                "capture_packet_processing_failed",
                error=str(exc),
                interface=session.interface,
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _record_drop_locked(self) -> None:
        """Increment the drop counter. Caller must hold _lock."""
        self._drop_count += 1

        if self._session is not None:
            self._session.drop_count = self._drop_count

    def _is_running_locked(self) -> bool:
        """Return whether capture workers are currently active."""
        capture_alive = (
            self._capture_worker is not None
            and self._capture_worker.is_alive()
        )

        processing_alive = (
            self._processing_worker is not None
            and self._processing_worker.is_alive()
        )

        return capture_alive and processing_alive

    @staticmethod
    def _join_worker(worker: Thread | None) -> None:
        """Join a worker unless it is the calling thread."""
        if worker is None:
            return

        if worker is current_thread():
            return

        if worker.is_alive():
            worker.join(ScapyCaptureAdapter._JOIN_TIMEOUT)

    def _should_stop(self, _packet: Any) -> bool:
        """Stop Scapy when the adapter lifecycle requests shutdown."""
        return self._stop_event.is_set()

    @staticmethod
    def _interface_exists(name: str) -> bool:
        """Return whether Scapy knows the requested interface."""
        try:
            conf.ifaces.dev_from_name(name)
            return True
        except (KeyError, ValueError, IndexError):
            return False
