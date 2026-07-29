"""TCP segment dissector."""

from __future__ import annotations

from packetanalyzer.domain.packet import Layer


def dissect_tcp(raw_layer: object) -> Layer:
    """Dissect a TCP segment layer.

    Args:
        raw_layer: The Scapy TCP layer object.

    Returns:
        A Layer domain object with TCP fields.

    Note:
        TCP payload bytes are included in raw_bytes but are NOT decoded
        or labeled as application data. This is consistent with the
        ethical policy in CONTRIBUTING.md (SR-10).
    """
    raise NotImplementedError("Implemented in Phase 3 — M1")
