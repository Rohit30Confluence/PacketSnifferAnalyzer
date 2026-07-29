"""TLS metadata dissector.

IMPORTANT: This dissector extracts TLS HANDSHAKE METADATA ONLY.
It does NOT decrypt TLS traffic and does NOT attempt to extract
application data from TLS records.

Extracted metadata includes:
  - TLS version
  - Handshake type (ClientHello, ServerHello, etc.)
  - Cipher suites offered (ClientHello)
  - Selected cipher suite (ServerHello)
  - SNI (Server Name Indication) from ClientHello
  - Certificate subject/issuer (from Certificate messages)

This is consistent with the security policy (SR-10) which prohibits
features designed to extract credentials or decrypt traffic.
"""

from __future__ import annotations

from packetanalyzer.domain.packet import Layer


def dissect_tls_metadata(raw_layer: object) -> Layer:
    """Dissect TLS handshake metadata from a TLS record.

    Args:
        raw_layer: The Scapy TLS layer object.

    Returns:
        A Layer domain object with TLS handshake metadata.
        Payload bytes are not included.
    """
    raise NotImplementedError("Implemented in Phase 3 — M1")
