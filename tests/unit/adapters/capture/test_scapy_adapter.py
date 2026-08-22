"""Unit tests for the Scapy capture adapter."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from scapy.interfaces import NetworkInterface

from packetanalyzer.adapters.capture.scapy_adapter import ScapyCaptureAdapter


class FakeFlags:
    """Minimal flag object matching the behavior used by the adapter."""

    def __init__(self, values: set[str]) -> None:
        self.values = values

    def __and__(self, value: str) -> bool:
        return value in self.values


def make_interface(
    name: str,
    *,
    description: str = "",
    flags: set[str] | None = None,
    ips: dict[int, list[str]] | None = None,
) -> MagicMock:
    """Create a minimal Scapy NetworkInterface test double."""
    interface = MagicMock(spec=NetworkInterface)
    interface.name = name
    interface.description = description
    interface.flags = FakeFlags(flags or {"UP"})
    interface.ips = ips or {}

    return interface


class TestScapyCaptureAdapter:
    """Tests for ScapyCaptureAdapter."""

    def test_list_interfaces_returns_scapy_interfaces(self) -> None:
        """Adapter converts Scapy interfaces into InterfaceInfo objects."""
        interface = make_interface(
            "en0",
            description="Wi-Fi",
            flags={"UP"},
            ips={
                4: ["192.168.1.10"],
                6: ["fe80::1234"],
            },
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=[interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert len(result) == 1
        assert result[0].name == "en0"
        assert result[0].description == "Wi-Fi"
        assert result[0].is_up is True
        assert result[0].is_loopback is False
        assert result[0].addresses == [
            "192.168.1.10",
            "fe80::1234",
        ]

    def test_loopback_interface_is_detected(self) -> None:
        """Loopback interfaces are marked correctly."""
        interface = make_interface(
            "lo0",
            flags={"UP", "LOOPBACK"},
            ips={
                4: ["127.0.0.1"],
                6: ["::1"],
            },
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=[interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert len(result) == 1
        assert result[0].name == "lo0"
        assert result[0].is_up is True
        assert result[0].is_loopback is True

    def test_empty_description_falls_back_to_interface_name(self) -> None:
        """An interface without a description uses its name."""
        interface = make_interface(
            "en0",
            description="",
            ips={4: ["192.168.1.10"]},
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=[interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert result[0].description == "en0"

    def test_non_network_interface_entries_are_ignored(self) -> None:
        """Unexpected entries in Scapy's interface collection are ignored."""
        interface = make_interface(
            "en0",
            ips={4: ["192.168.1.10"]},
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=["unexpected-entry", interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert len(result) == 1
        assert result[0].name == "en0"

    def test_unspecified_addresses_are_filtered(self) -> None:
        """Unspecified IPv4 and IPv6 addresses are excluded."""
        interface = make_interface(
            "en0",
            ips={
                4: [
                    "0.0.0.0",
                    "192.168.1.10",
                ],
                6: [
                    "::",
                    "fe80::1234",
                ],
            },
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=[interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert result[0].addresses == [
            "192.168.1.10",
            "fe80::1234",
        ]
