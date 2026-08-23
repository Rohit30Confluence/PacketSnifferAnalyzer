"""CLI commands for live packet capture."""

from __future__ import annotations

import signal
import time
import uuid
from datetime import datetime, timezone
from typing import Any

import click

from packetanalyzer import __version__
from packetanalyzer.domain.packet import Packet
from packetanalyzer.domain.session import CaptureSession
from packetanalyzer.infrastructure.audit import AuditLogger
from packetanalyzer.infrastructure.config import get_settings
from packetanalyzer.interfaces.cli.formatters import format_json, print_error
from packetanalyzer.use_cases.capture_session_manager import CaptureSessionManager


class InMemoryCaptureStorage:
    """M2 capture sink.

    M2 owns live capture and session statistics.
    Persistent PCAP storage is intentionally deferred to M3.
    """

    def __init__(self) -> None:
        self.sessions: dict[str, CaptureSession] = {}
        self.packets: dict[str, list[Packet]] = {}

    def open_session(self, session: CaptureSession) -> None:
        if session.session_id in self.sessions:
            raise RuntimeError(
                f"Session '{session.session_id}' already exists"
            )

        self.sessions[session.session_id] = session
        self.packets[session.session_id] = []

    def write_packet(self, packet: Packet) -> None:
        if packet.session_id not in self.packets:
            raise RuntimeError(
                f"Unknown session '{packet.session_id}'"
            )

        self.packets[packet.session_id].append(packet)

    def close_session(self, session: CaptureSession) -> None:
        return None

    def read_packets(
        self,
        session_id: str,
        offset: int = 0,
        limit: int | None = None,
    ):
        packets = self.packets.get(session_id, [])
        selected = packets[offset:]

        if limit is not None:
            selected = selected[:limit]

        yield from selected

    def list_sessions(self) -> list[CaptureSession]:
        return list(self.sessions.values())

    def delete_session(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)
        self.packets.pop(session_id, None)


class LiveCaptureRuntime:
    """Own the M2 application runtime for one foreground capture."""

    def __init__(self) -> None:
        settings = get_settings()

        from packetanalyzer.adapters.capture.scapy_adapter import ScapyCaptureAdapter
        from packetanalyzer.adapters.dissection.scapy_dissector import ScapyDissector

        self.storage = InMemoryCaptureStorage()
        self.capture = ScapyCaptureAdapter(ScapyDissector())
        self.audit = AuditLogger(settings.log_dir / "audit.ndjson")

        self.manager = CaptureSessionManager(
            capture_port=self.capture,
            storage_port=self.storage,
            audit_logger=self.audit,
        )

    def start(
        self,
        session: CaptureSession,
        count: int,
    ) -> None:
        def packet_callback(packet: Packet) -> None:
            self.storage.write_packet(packet)

            session.packet_count += 1
            session.byte_count += packet.length

            click.echo(
                f"[{session.packet_count}] "
                f"{packet.length} bytes "
                f"{packet.interface}"
            )

            if count and session.packet_count >= count:
                self.manager.stop()

        self.manager.start(session, packet_callback)

    def stop(self) -> CaptureSession | None:
        if self.manager.active_session is None:
            return None

        return self.manager.stop()

    def pause(self) -> CaptureSession:
        return self.manager.pause()

    def resume(self) -> CaptureSession:
        return self.manager.resume()

    def status(self) -> CaptureSession | None:
        self.manager.refresh_statistics()
        return self.manager.status()


def _session_dict(session: CaptureSession) -> dict[str, Any]:
    return {
        "session_id": session.session_id,
        "name": session.name,
        "interface": session.interface,
        "bpf_filter": session.bpf_filter,
        "state": session.state.name,
        "started_at": session.started_at.isoformat(),
        "stopped_at": (
            session.stopped_at.isoformat()
            if session.stopped_at
            else None
        ),
        "packet_count": session.packet_count,
        "byte_count": session.byte_count,
        "drop_count": session.drop_count,
        "operator": session.operator,
        "tool_version": session.tool_version,
        "pcap_path": session.pcap_path,
        "encrypted": session.encrypted,
    }


def _make_session(
    interface: str,
    bpf_filter: str,
    name: str | None,
) -> CaptureSession:
    return CaptureSession(
        session_id=str(uuid.uuid4()),
        name=name
        or (
            "capture-"
            + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        ),
        interface=interface,
        bpf_filter=bpf_filter,
        started_at=datetime.now(timezone.utc),
        operator="",
        tool_version=__version__,
    )


@click.group(name="capture")
def capture() -> None:
    """Manage live packet capture sessions."""


@capture.command(name="start")
@click.option(
    "--interface",
    "-i",
    required=True,
    help="Network interface to capture on.",
)
@click.option(
    "--filter",
    "-f",
    "bpf_filter",
    default="",
    help="BPF capture filter.",
)
@click.option(
    "--name",
    "-n",
    default=None,
    help="Human-readable session name.",
)
@click.option(
    "--count",
    "-c",
    default=0,
    type=click.IntRange(min=0),
    help="Stop after N packets; 0 means unlimited.",
)
@click.option(
    "--output",
    "-o",
    default=None,
    type=click.Path(dir_okay=False),
    help="PCAP output is available in M3.",
)
@click.option(
    "--encrypt",
    is_flag=True,
    default=False,
    help="PCAP encryption is available in M3.",
)
def capture_start(
    interface: str,
    bpf_filter: str,
    name: str | None,
    count: int,
    output: str | None,
    encrypt: bool,
) -> None:
    """Start a foreground live capture."""

    if output is not None:
        raise click.ClickException(
            "PCAP output is an M3 feature. "
            "M2 provides live capture and analysis only."
        )

    if encrypt:
        raise click.ClickException(
            "PCAP encryption is an M3 feature."
        )

    runtime = LiveCaptureRuntime()
    session = _make_session(interface, bpf_filter, name)

    def shutdown(signum: int, _frame: Any) -> None:
        click.echo(
            f"\nReceived signal {signum}; stopping capture...",
            err=True,
        )

        try:
            runtime.stop()
        except Exception as exc:  # noqa: BLE001
            print_error(f"Capture shutdown failed: {exc}")

    old_sigint = signal.signal(signal.SIGINT, shutdown)
    old_sigterm = signal.signal(signal.SIGTERM, shutdown)

    try:
        try:
            runtime.start(session, count)
        except Exception as exc:  # noqa: BLE001
            raise click.ClickException(
                f"Unable to start capture: {exc}"
            ) from exc

        click.echo(
            f"Capture started\n"
            f"  session:   {session.session_id}\n"
            f"  interface: {session.interface}\n"
            f"  filter:    {session.bpf_filter or '(none)'}"
        )

        while runtime.manager.active_session is not None:
            time.sleep(0.05)

        click.echo(
            f"Capture stopped\n"
            f"  packets: {session.packet_count}\n"
            f"  bytes:   {session.byte_count}\n"
            f"  drops:   {session.drop_count}"
        )

    finally:
        if runtime.manager.active_session is not None:
            try:
                runtime.stop()
            except Exception:
                pass

        signal.signal(signal.SIGINT, old_sigint)
        signal.signal(signal.SIGTERM, old_sigterm)


@capture.command(name="stop")
def capture_stop() -> None:
    """Stop a capture running in this process."""

    raise click.ClickException(
        "No persistent capture daemon exists in M2. "
        "Run capture in the foreground and press Ctrl+C."
    )


@capture.command(name="pause")
def capture_pause() -> None:
    """Pause a capture running in this process."""

    raise click.ClickException(
        "Pause is process-local in M2. "
        "It must be issued by the process owning the capture."
    )


@capture.command(name="resume")
def capture_resume() -> None:
    """Resume a capture running in this process."""

    raise click.ClickException(
        "Resume is process-local in M2. "
        "It must be issued by the process owning the capture."
    )


@capture.command(name="status")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Output JSON.",
)
def capture_status(output_json: bool) -> None:
    """Show capture runtime status."""

    payload = {
        "state": "STOPPED",
        "active_session": None,
        "runtime": "foreground",
        "persistent_runtime": False,
        "message": (
            "M2 capture is foreground-owned. "
            "Persistent runtime control is an M3 concern."
        ),
    }

    if output_json:
        click.echo(format_json(payload))
        return

    click.echo("State: STOPPED")
    click.echo("Active session: none")
    click.echo("Runtime: foreground")
    click.echo(payload["message"])
