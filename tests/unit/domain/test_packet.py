"""Unit tests for the Packet domain model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packetanalyzer.domain.packet import Layer, Packet


@pytest.mark.unit
class TestLayer:
    """Tests for the Layer domain model."""

    def test_layer_creation(self) -> None:
        """Layer can be created with protocol and fields."""
        layer = Layer(
            protocol="TCP",
            fields={"sport": 80, "dport": 54321},
        )
        assert layer.protocol == "TCP"
        assert layer.fields["sport"] == 80

    def test_layer_get_field_existing(self) -> None:
        """get_field returns the value for an existing field."""
        layer = Layer(protocol="IPv4", fields={"ttl": 64})
        assert layer.get_field("ttl") == 64

    def test_layer_get_field_missing_returns_default(self) -> None:
        """get_field returns the default for a missing field."""
        layer = Layer(protocol="IPv4", fields={})
        assert layer.get_field("ttl") is None
        assert layer.get_field("ttl", default=128) == 128

    def test_layer_is_frozen(self) -> None:
        """Layer is immutable (frozen dataclass)."""
        layer = Layer(protocol="TCP", fields={})
        with pytest.raises(AttributeError):
            layer.protocol = "UDP"  # type: ignore[misc]


@pytest.mark.unit
class TestPacket:
    """Tests for the Packet domain model."""

    def test_packet_creation(self, sample_packet: Packet) -> None:
        """Packet can be created with all required fields."""
        assert sample_packet.packet_id == 1
        assert sample_packet.interface == "eth0"
        assert sample_packet.length == 74

    def test_packet_is_complete_when_fully_captured(self, sample_packet: Packet) -> None:
        """is_complete returns True when captured_length >= length."""
        assert sample_packet.is_complete is True

    def test_packet_is_not_complete_when_truncated(self) -> None:
        """is_complete returns False when packet is truncated."""
        packet = Packet(
            packet_id=1,
            timestamp=datetime.now(tz=timezone.utc),
            interface="eth0",
            length=1500,
            captured_length=64,  # Truncated
            layers=(),
            raw_bytes=b"\x00" * 64,
            session_id="test",
        )
        assert packet.is_complete is False

    def test_packet_has_no_parse_error_by_default(self, sample_packet: Packet) -> None:
        """has_parse_error returns False when no error occurred."""
        assert sample_packet.has_parse_error is False

    def test_packet_has_parse_error_when_set(self) -> None:
        """has_parse_error returns True when parse_error is set."""
        packet = Packet(
            packet_id=1,
            timestamp=datetime.now(tz=timezone.utc),
            interface="eth0",
            length=100,
            captured_length=100,
            layers=(),
            raw_bytes=b"\x00" * 100,
            session_id="test",
            parse_error="Unexpected end of TCP header",
        )
        assert packet.has_parse_error is True
        assert packet.parse_error == "Unexpected end of TCP header"

    def test_get_layer_returns_matching_layer(self, sample_packet: Packet) -> None:
        """get_layer returns the first layer matching the protocol name."""
        layer = sample_packet.get_layer("TCP")
        assert layer is not None
        assert layer.protocol == "TCP"

    def test_get_layer_case_insensitive(self, sample_packet: Packet) -> None:
        """get_layer is case-insensitive."""
        assert sample_packet.get_layer("tcp") is not None
        assert sample_packet.get_layer("TCP") is not None
        assert sample_packet.get_layer("Tcp") is not None

    def test_get_layer_returns_none_for_missing_protocol(self, sample_packet: Packet) -> None:
        """get_layer returns None when the protocol is not present."""
        assert sample_packet.get_layer("DNS") is None

    def test_has_layer_true_for_present_protocol(self, sample_packet: Packet) -> None:
        """has_layer returns True for a protocol that is present."""
        assert sample_packet.has_layer("IPv4") is True

    def test_has_layer_false_for_absent_protocol(self, sample_packet: Packet) -> None:
        """has_layer returns False for a protocol that is not present."""
        assert sample_packet.has_layer("DNS") is False

    def test_summary_returns_string(self, sample_packet: Packet) -> None:
        """summary() returns a non-empty string."""
        summary = sample_packet.summary()
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert "#1" in summary
