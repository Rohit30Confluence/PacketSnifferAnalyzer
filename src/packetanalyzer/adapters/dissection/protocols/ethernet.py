"""Ethernet frame dissector."""

from __future__ import annotations

from packetanalyzer.domain.packet import Layer


def dissect_ethernet(raw_layer: object) -> Layer:
    """Dissect an Ethernet frame layer.

    Args:
        raw_layer: The Scapy Ether layer object.

    Returns:
        A Layer domain object with Ethernet fields.
    """
    raise NotImplementedError("Implemented in Phase 3 — M1")
