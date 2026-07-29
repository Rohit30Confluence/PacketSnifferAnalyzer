"""Example plugin: HTTP Path Logger.

This example plugin demonstrates how to write a PacketSnifferAnalyzer plugin.
It logs the HTTP request path from HTTP/1.x GET and POST requests.

IMPORTANT: This plugin logs request PATHS only, not headers, bodies,
or any other content. It does not log credentials or personal data.
This is consistent with the ethical policy in CONTRIBUTING.md.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from packetanalyzer.plugins.interface import PluginInterface
from packetanalyzer.infrastructure.logging import get_logger

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet

logger = get_logger(__name__)


class HttpPathLoggerPlugin(PluginInterface):
    """Example plugin that logs HTTP request paths.

    This plugin demonstrates:
    - Implementing PluginInterface
    - Accessing packet layers
    - Structured logging from a plugin
    - Ethical data handling (paths only, no payloads)
    """

    @property
    def name(self) -> str:
        return "http_path_logger"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return (
            "Logs HTTP/1.x request paths (method + path only). "
            "Does not log headers, bodies, or credentials."
        )

    def on_load(self) -> None:
        logger.info("plugin_loaded", plugin=self.name)

    def on_unload(self) -> None:
        logger.info("plugin_unloaded", plugin=self.name)

    def analyze_packet(self, packet: "Packet") -> None:
        """Log the HTTP request path if this is an HTTP request packet."""
        # Implementation will be added in Phase 3 — M6
        # The plugin will inspect the TCP payload for HTTP/1.x request lines
        # and log only the method and path (e.g., 'GET /api/v1/users').
        # It will never log Authorization headers, cookies, or body content.
