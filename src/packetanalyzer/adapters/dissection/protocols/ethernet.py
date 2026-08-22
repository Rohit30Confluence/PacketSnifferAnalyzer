"""Ethernet frame dissector."""

from __future__ import annotations

from typing import Any

from packetanalyzer.domain.packet import Layer


def dissect_ethernet(raw_layer: object) -> Layer:
    """Dissect a Scapy Ethernet layer into a domain Layer.

    Args:
        raw_layer: The Scapy Ether layer object.

    Returns:
        A Layer containing normalized Ethernet metadata.

    Raises:
        TypeError: If the supplied object does not expose the expected
            Ethernet fields.
    """
    try:
        src = str(getattr(raw_layer, "src"))
        dst = str(getattr(raw_layer, "dst"))
        ether_type = int(getattr(raw_layer, "type"))
        raw_bytes = bytes(raw_layer)
    except (AttributeError, TypeError, ValueError) as exc:
        raise TypeError("Invalid Scapy Ethernet layer") from exc

    fields: dict[str, Any] = {
        "src": src,
        "dst": dst,
        "type": ether_type,
    }

    return Layer(
        protocol="Ethernet",
        fields=fields,
        raw_bytes=raw_bytes,
    )
