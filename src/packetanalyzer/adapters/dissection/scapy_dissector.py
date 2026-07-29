"""Scapy-based protocol dissection adapter.

This adapter implements DissectorPort using Scapy's packet parsing
capabilities. It decodes protocol layers from raw bytes and produces
structured Packet domain objects.

Error handling:
    Malformed or truncated packets are caught at each layer boundary.
    The packet is returned with whatever layers were successfully decoded,
    and parse_error is set to describe the failure. The capture loop
    is never interrupted by a dissection error.
"""

from __future__ import annotations

from packetanalyzer.ports.dissector_port import DissectorPort
from packetanalyzer.domain.packet import Packet
from packetanalyzer.infrastructure.logging import get_logger

logger = get_logger(__name__)


class ScapyDissector(DissectorPort):
    """Protocol dissector using Scapy.

    This is a scaffold. The full implementation will be added in
    Milestone 1 (Epic 2, Issue 2.4).
    """

    def dissect(self, raw: bytes, session_id: str, packet_id: int, interface: str) -> Packet:
        """Dissect raw bytes into a structured Packet."""
        raise NotImplementedError("Implemented in Phase 3 — M1")

    def supported_protocols(self) -> list[str]:
        """Return the list of protocols this dissector supports."""
        return [
            "Ethernet",
            "ARP",
            "IPv4",
            "IPv6",
            "TCP",
            "UDP",
            "ICMP",
            "ICMPv6",
            "DNS",
            "DHCP",
            "VLAN",
            "TLS",
        ]
