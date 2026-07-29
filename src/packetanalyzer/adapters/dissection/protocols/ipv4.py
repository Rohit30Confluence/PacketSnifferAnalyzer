"""IPv4 packet dissector."""

from __future__ import annotations

from packetanalyzer.domain.packet import Layer


def dissect_ipv4(raw_layer: object) -> Layer:
    """Dissect an IPv4 packet layer.

    Args:
        raw_layer: The Scapy IP layer object.

    Returns:
        A Layer domain object with IPv4 fields.
    """
    raise NotImplementedError("Implemented in Phase 3 — M1")
