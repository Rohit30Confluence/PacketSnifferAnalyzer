# Example Plugin: DNS Query Logger
#
# This example plugin logs DNS query names from captured traffic.
# It demonstrates a more complete plugin than the built-in http_path_logger.
#
# IMPORTANT: This plugin logs DNS query NAMES only (e.g., "example.com").
# It does not log DNS responses, IP addresses resolved, or any other data.
# This is consistent with the ethical policy in CONTRIBUTING.md.
#
# Installation:
#   Copy this directory to the plugins/ directory at the project root.
#   The plugin manager will discover it automatically at startup.

from __future__ import annotations

from typing import TYPE_CHECKING

from packetanalyzer.plugins.interface import PluginInterface
from packetanalyzer.infrastructure.logging import get_logger

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet

logger = get_logger(__name__)


class DnsQueryLoggerPlugin(PluginInterface):
    """Example plugin that logs DNS query names.

    Logs only the query name (e.g., 'example.com') from DNS queries.
    Does not log DNS responses, resolved IP addresses, or any other data.
    """

    def __init__(self) -> None:
        self._query_count = 0

    @property
    def name(self) -> str:
        return "dns_query_logger"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return (
            "Logs DNS query names from captured traffic. "
            "Logs query names only — not responses or resolved addresses."
        )

    def on_load(self) -> None:
        logger.info("plugin_loaded", plugin=self.name)
        self._query_count = 0

    def on_unload(self) -> None:
        logger.info(
            "plugin_unloaded",
            plugin=self.name,
            total_queries_logged=self._query_count,
        )

    def analyze_packet(self, packet: "Packet") -> None:
        """Log DNS query names from DNS packets."""
        dns_layer = packet.get_layer("DNS")
        if dns_layer is None:
            return

        # Only process queries (QR=0), not responses (QR=1)
        qr = dns_layer.get_field("qr", 1)
        if qr != 0:
            return

        qname = dns_layer.get_field("qname")
        if qname:
            self._query_count += 1
            logger.info(
                "dns_query",
                plugin=self.name,
                qname=str(qname),
                session_id=packet.session_id,
            )
