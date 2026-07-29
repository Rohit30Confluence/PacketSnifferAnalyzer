"""Plugin interface contract.

All plugins must implement this abstract base class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet, Layer


class PluginInterface(ABC):
    """Abstract base class for PacketSnifferAnalyzer plugins.

    A plugin can provide:
    - Custom protocol dissectors (via dissect_layer)
    - Post-dissection packet analysis (via analyze_packet)

    Plugins are loaded from the plugins/ directory at startup.
    Each plugin must implement at minimum: name, version, and description.

    Example:
        See src/packetanalyzer/plugins/examples/http_path_logger/ for
        a complete example plugin.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of this plugin."""

    @property
    @abstractmethod
    def version(self) -> str:
        """The version of this plugin (SemVer string)."""

    @property
    @abstractmethod
    def description(self) -> str:
        """A brief description of what this plugin does."""

    @property
    def protocols(self) -> list[str]:
        """Protocol names this plugin can dissect.

        Return an empty list if this plugin does not add dissectors.
        """
        return []

    def on_load(self) -> None:
        """Called when the plugin is loaded. Override for initialization."""

    def on_unload(self) -> None:
        """Called when the plugin is unloaded. Override for cleanup."""

    def dissect_layer(self, protocol: str, raw: bytes) -> "Layer | None":
        """Attempt to dissect a protocol layer.

        Args:
            protocol: The protocol name to dissect.
            raw: The raw bytes for this layer.

        Returns:
            A Layer domain object if this plugin handles the protocol,
            or None if it does not.
        """
        return None

    def analyze_packet(self, packet: "Packet") -> None:
        """Perform post-dissection analysis on a packet.

        This method is called for every packet after dissection.
        It must be non-blocking and must not modify the packet.

        Args:
            packet: The fully dissected packet.
        """
