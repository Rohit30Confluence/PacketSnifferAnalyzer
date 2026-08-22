"""TCP segment dissector."""

from __future__ import annotations

from typing import Any

from packetanalyzer.domain.packet import Layer


def dissect_tcp(raw_layer: object) -> Layer:
    """Dissect a Scapy TCP layer into a domain Layer.

    Args:
        raw_layer: The Scapy TCP layer object.

    Returns:
        A Layer containing normalized TCP metadata.

    Raises:
        TypeError: If the supplied object does not expose the expected
            TCP fields.
    """
    try:
        raw_bytes = bytes(raw_layer)

        sport = int(getattr(raw_layer, "sport"))
        dport = int(getattr(raw_layer, "dport"))
        seq = int(getattr(raw_layer, "seq"))
        ack = int(getattr(raw_layer, "ack"))
        flags = str(getattr(raw_layer, "flags"))
        window = int(getattr(raw_layer, "window"))
        data_offset_value = getattr(raw_layer, "dataofs")

        if data_offset_value is None:
            data_offset = 5
        else:
            data_offset = int(data_offset_value)

    except (AttributeError, TypeError, ValueError) as exc:
        raise TypeError("Invalid Scapy TCP layer") from exc

    fields: dict[str, Any] = {
        "sport": sport,
        "dport": dport,
        "seq": seq,
        "ack": ack,
        "flags": flags,
        "window": window,
        "data_offset": data_offset,
    }

    return Layer(
        protocol="TCP",
        fields=fields,
        raw_bytes=raw_bytes,
    )
