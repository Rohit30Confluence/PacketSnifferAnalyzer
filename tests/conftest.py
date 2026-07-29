"""Shared pytest fixtures for PacketSnifferAnalyzer tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from packetanalyzer.domain.packet import Layer, Packet
from packetanalyzer.domain.session import CaptureSession, SessionState
from packetanalyzer.domain.flow import Flow, FlowState
from packetanalyzer.domain.alert import AlertRule, AlertSeverity, AlertAction


# =============================================================================
# Fixtures: Paths
# =============================================================================

@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_pcap(fixtures_dir: Path) -> Path:
    """Return the path to the sample PCAP fixture."""
    return fixtures_dir / "sample.pcap"


@pytest.fixture
def malformed_pcap(fixtures_dir: Path) -> Path:
    """Return the path to the malformed PCAP fixture."""
    return fixtures_dir / "malformed.pcap"


# =============================================================================
# Fixtures: Domain Objects
# =============================================================================

@pytest.fixture
def sample_layer() -> Layer:
    """Return a sample Ethernet Layer."""
    return Layer(
        protocol="Ethernet",
        fields={
            "src": "aa:bb:cc:dd:ee:ff",
            "dst": "11:22:33:44:55:66",
            "type": 0x0800,
        },
        raw_bytes=b"\xaa\xbb\xcc\xdd\xee\xff\x11\x22\x33\x44\x55\x66\x08\x00",
    )


@pytest.fixture
def sample_ipv4_layer() -> Layer:
    """Return a sample IPv4 Layer."""
    return Layer(
        protocol="IPv4",
        fields={
            "src": "192.168.1.100",
            "dst": "8.8.8.8",
            "ttl": 64,
            "proto": 6,
            "version": 4,
            "ihl": 5,
        },
        raw_bytes=b"\x45\x00\x00\x28" + b"\x00" * 16,
    )


@pytest.fixture
def sample_tcp_layer() -> Layer:
    """Return a sample TCP Layer."""
    return Layer(
        protocol="TCP",
        fields={
            "sport": 54321,
            "dport": 443,
            "seq": 1000,
            "ack": 2000,
            "flags": "S",
            "window": 65535,
        },
        raw_bytes=b"\xd4\x31\x01\xbb" + b"\x00" * 16,
    )


@pytest.fixture
def sample_packet(sample_layer: Layer, sample_ipv4_layer: Layer, sample_tcp_layer: Layer) -> Packet:
    """Return a sample fully-dissected Packet."""
    return Packet(
        packet_id=1,
        timestamp=datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
        interface="eth0",
        length=74,
        captured_length=74,
        layers=(sample_layer, sample_ipv4_layer, sample_tcp_layer),
        raw_bytes=b"\x00" * 74,
        session_id="test-session-001",
    )


@pytest.fixture
def sample_session() -> CaptureSession:
    """Return a sample CaptureSession."""
    return CaptureSession(
        session_id="test-session-001",
        name="Test Session",
        interface="eth0",
        bpf_filter="tcp port 443",
        started_at=datetime(2024, 1, 15, 10, 0, 0, tzinfo=timezone.utc),
        state=SessionState.RUNNING,
        operator="testuser",
        tool_version="0.1.0-alpha.1",
    )


@pytest.fixture
def sample_alert_rule() -> AlertRule:
    """Return a sample AlertRule."""
    return AlertRule(
        rule_id="rule-001",
        name="SYN Flood Detection",
        description="Detects SYN flood attacks by monitoring SYN packet rate.",
        condition="syn_flood",
        threshold=1000.0,
        window_seconds=10,
        severity=AlertSeverity.HIGH,
        actions=frozenset({AlertAction.CONSOLE, AlertAction.LOG}),
    )


# =============================================================================
# Fixtures: Mocks
# =============================================================================

@pytest.fixture
def mock_capture_port() -> MagicMock:
    """Return a mock CapturePort."""
    from packetanalyzer.ports.capture_port import CapturePort
    mock = MagicMock(spec=CapturePort)
    mock.get_drop_count.return_value = 0
    return mock


@pytest.fixture
def mock_storage_port() -> MagicMock:
    """Return a mock StoragePort."""
    from packetanalyzer.ports.storage_port import StoragePort
    return MagicMock(spec=StoragePort)


@pytest.fixture
def mock_audit_logger() -> MagicMock:
    """Return a mock AuditLogger."""
    from packetanalyzer.infrastructure.audit import AuditLogger
    return MagicMock(spec=AuditLogger)
