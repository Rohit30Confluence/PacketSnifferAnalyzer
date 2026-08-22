"""IPv4 packet dissector."""

from __future__ import annotations

from typing import Any

from packetanalyzer.domain.packet import Layer


def dissect_ipv4(raw_layer: object) -> Layer:
    """Dissect a Scapy IPv4 layer into a domain Layer.

    Args:
        raw_layer: The Scapy IP layer object.

    Returns:
        A Layer containing normalized IPv4 metadata.

    Raises:
        TypeError: If the supplied object does not expose the expected
            IPv4 fields.
    """
    try:
        # Serialize first so Scapy calculates derived header fields such
        # as IHL before they are read.
        raw_bytes = bytes(raw_layer)

        version = int(getattr(raw_layer, "version"))
        ihl_value = getattr(raw_layer, "ihl")
        ttl = int(getattr(raw_layer, "ttl"))
        proto = int(getattr(raw_layer, "proto"))
        src = str(getattr(raw_layer, "src"))
        dst = str(getattr(raw_layer, "dst"))

        if ihl_value is None:
            ihl = 5
        else:
            ihl = int(ihl_value)

    except (AttributeError, TypeError, ValueError) as exc:
        raise TypeError("Invalid Scapy IPv4 layer") from exc

    fields: dict[str, Any] = {
        "version": version,
        "ihl": ihl,
        "ttl": ttl,
        "proto": proto,
        "src": src,
        "dst": dst,
    }

    return Layer(
        protocol="IPv4",
        fields=fields,
        raw_bytes=raw_bytes,
    )
