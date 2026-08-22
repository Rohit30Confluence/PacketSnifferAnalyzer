"""UDP datagram dissector."""

from __future__ import annotations

from typing import Any

from packetanalyzer.domain.packet import Layer


def dissect_udp(raw_layer: object) -> Layer:
    """Dissect a Scapy UDP layer into a domain Layer.

    Args:
        raw_layer: The Scapy UDP layer object.

    Returns:
        A Layer containing normalized UDP metadata.

    Raises:
        TypeError: If the supplied object does not expose the expected
            UDP fields.
    """
    try:
        # Serialize first so Scapy calculates derived fields such as
        # length and checksum.
        raw_bytes = bytes(raw_layer)

        sport = int(getattr(raw_layer, "sport"))
        dport = int(getattr(raw_layer, "dport"))

        length_value = getattr(raw_layer, "len")
        checksum_value = getattr(raw_layer, "chksum")

        if length_value is None:
            length = len(raw_bytes)
        else:
            length = int(length_value)

        if checksum_value is None:
            checksum = 0
        else:
            checksum = int(checksum_value)

    except (AttributeError, TypeError, ValueError) as exc:
        raise TypeError("Invalid Scapy UDP layer") from exc

    fields: dict[str, Any] = {
        "sport": sport,
        "dport": dport,
        "length": length,
        "checksum": checksum,
    }

    return Layer(
        protocol="UDP",
        fields=fields,
        raw_bytes=raw_bytes,
    )
