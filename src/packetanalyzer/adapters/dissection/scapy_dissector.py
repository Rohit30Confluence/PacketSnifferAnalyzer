"""Scapy-based protocol dissection adapter."""

from __future__ import annotations

from datetime import datetime, timezone

from scapy.packet import NoPayload
from scapy.all import Ether

from packetanalyzer.adapters.dissection.protocols.ethernet import dissect_ethernet
from packetanalyzer.adapters.dissection.protocols.ipv4 import dissect_ipv4
from packetanalyzer.adapters.dissection.protocols.tcp import dissect_tcp
from packetanalyzer.adapters.dissection.protocols.udp import dissect_udp
from packetanalyzer.domain.packet import Layer, Packet
from packetanalyzer.infrastructure.logging import get_logger
from packetanalyzer.ports.dissector_port import DissectorPort

logger = get_logger(__name__)


class ScapyDissector(DissectorPort):
    """Protocol dissector using Scapy."""

    _PROTOCOL_DISSECTORS = {
        "Ethernet": dissect_ethernet,
        "IPv4": dissect_ipv4,
        "TCP": dissect_tcp,
	"UDP": dissect_udp,
    }

    def dissect(
        self,
        raw: bytes,
        session_id: str,
        packet_id: int,
        interface: str,
    ) -> Packet:
        """Dissect raw bytes into a structured Packet.

        Dissection errors are captured in ``parse_error`` rather than
        propagated, allowing the capture pipeline to continue processing
        subsequent packets.
        """
        timestamp = datetime.now(timezone.utc)
        layers: list[Layer] = []
        parse_error: str | None = None

        try:
            if not raw:
                raise ValueError("Empty packet data")

            packet = Ether(raw)

            current = packet

            while current is not None and not isinstance(current, NoPayload):
                protocol = self._protocol_name(current)

                dissector = self._PROTOCOL_DISSECTORS.get(protocol)

                if dissector is not None:
                    try:
                        layer = dissector(current)
                        layers.append(layer)
                    except (AttributeError, TypeError, ValueError) as exc:
                        parse_error = (
                            f"{protocol} dissection failed: {exc}"
                        )
                        logger.warning(
                            "packet_layer_dissection_failed",
                            protocol=protocol,
                            error=str(exc),
                        )
                        break

                next_layer = getattr(current, "payload", None)

                if next_layer is None or isinstance(next_layer, NoPayload):
                    break

                current = next_layer

        except (TypeError, ValueError, IndexError) as exc:
            parse_error = f"Packet dissection failed: {exc}"
            logger.warning(
                "packet_dissection_failed",
                error=str(exc),
            )

        return Packet(
            packet_id=packet_id,
            timestamp=timestamp,
            interface=interface,
            length=len(raw),
            captured_length=len(raw),
            layers=tuple(layers),
            raw_bytes=raw,
            session_id=session_id,
            parse_error=parse_error,
        )

    @staticmethod
    def _protocol_name(layer: object) -> str:
        """Return the normalized domain protocol name for a Scapy layer."""
        name = layer.__class__.__name__

        mapping = {
            "Ether": "Ethernet",
            "IP": "IPv4",
            "TCP": "TCP",
        }

        return mapping.get(name, name)

    def supported_protocols(self) -> list[str]:
        """Return protocols with implemented domain-layer dissectors."""
        return [
            "Ethernet",
            "IPv4",
            "TCP",
            "UDP",
        ]
