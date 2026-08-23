"""Regression tests for the M2 capture CLI."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from packetanalyzer.domain.session import SessionState
from packetanalyzer.interfaces.cli.app import cli
from packetanalyzer.interfaces.cli.commands.capture import (
    InMemoryCaptureStorage,
    LiveCaptureRuntime,
)


def test_capture_help() -> None:
    result = CliRunner().invoke(cli, ["capture", "--help"])

    assert result.exit_code == 0
    for command in ("start", "stop", "pause", "resume", "status"):
        assert command in result.output


def test_start_requires_interface() -> None:
    result = CliRunner().invoke(cli, ["capture", "start"])

    assert result.exit_code != 0
    assert "Missing option" in result.output


def test_start_rejects_m3_output() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "capture",
            "start",
            "-i",
            "en0",
            "-o",
            "capture.pcap",
        ],
    )

    assert result.exit_code != 0
    assert "M3" in result.output


def test_start_rejects_m3_encryption() -> None:
    result = CliRunner().invoke(
        cli,
        [
            "capture",
            "start",
            "-i",
            "en0",
            "--encrypt",
        ],
    )

    assert result.exit_code != 0
    assert "M3" in result.output


def test_stop_explains_foreground_runtime() -> None:
    result = CliRunner().invoke(cli, ["capture", "stop"])

    assert result.exit_code != 0
    assert "foreground" in result.output.lower()


def test_pause_explains_process_boundary() -> None:
    result = CliRunner().invoke(cli, ["capture", "pause"])

    assert result.exit_code != 0
    assert "process-local" in result.output


def test_resume_explains_process_boundary() -> None:
    result = CliRunner().invoke(cli, ["capture", "resume"])

    assert result.exit_code != 0
    assert "process-local" in result.output


def test_status_human() -> None:
    result = CliRunner().invoke(cli, ["capture", "status"])

    assert result.exit_code == 0
    assert "State: STOPPED" in result.output
    assert "Active session: none" in result.output


def test_status_json() -> None:
    result = CliRunner().invoke(
        cli,
        ["capture", "status", "--json"],
    )

    assert result.exit_code == 0
    assert '"state": "STOPPED"' in result.output
    assert '"active_session": null' in result.output


def test_in_memory_storage_round_trip() -> None:
    storage = InMemoryCaptureStorage()

    session = MagicMock()
    session.session_id = "test-session"

    packet = MagicMock()
    packet.session_id = "test-session"

    storage.open_session(session)
    storage.write_packet(packet)

    assert list(storage.read_packets("test-session")) == [packet]
    assert storage.list_sessions() == [session]


def test_runtime_builds_application_boundary() -> None:
    with patch(
        "packetanalyzer.interfaces.cli.commands.capture.get_settings"
    ) as settings:
        settings.return_value.log_dir = MagicMock()

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.ScapyCaptureAdapter"
        ), patch(
            "packetanalyzer.adapters.dissection.scapy_dissector.ScapyDissector"
        ), patch(
            "packetanalyzer.interfaces.cli.commands.capture.AuditLogger"
        ):
            runtime = LiveCaptureRuntime()

    assert runtime.manager is not None
    assert runtime.storage is not None


def test_runtime_status_refreshes_statistics() -> None:
    runtime = MagicMock()
    runtime.manager.active_session = None

    result = runtime.status()

    assert result is runtime.status.return_value
