"""Plugin manager — discovery, validation, and lifecycle management."""

from __future__ import annotations

import importlib
import importlib.util
from pathlib import Path
from typing import TYPE_CHECKING

from packetanalyzer.plugins.interface import PluginInterface
from packetanalyzer.infrastructure.logging import get_logger

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet

logger = get_logger(__name__)


class PluginManager:
    """Manages the lifecycle of PacketSnifferAnalyzer plugins.

    Discovers plugins from a directory, validates them against the
    PluginInterface contract, and manages their load/unload lifecycle.
    Plugin errors are isolated — a failing plugin is disabled without
    affecting the core engine.

    Args:
        plugin_dir: Directory to scan for plugins.
    """

    def __init__(self, plugin_dir: Path) -> None:
        self._plugin_dir = plugin_dir
        self._plugins: dict[str, PluginInterface] = {}
        self._disabled: set[str] = set()

    def discover(self) -> list[str]:
        """Scan the plugin directory and load all valid plugins.

        Returns:
            A list of successfully loaded plugin names.
        """
        raise NotImplementedError("Implemented in Phase 3 — M6")

    def get_plugin(self, name: str) -> PluginInterface | None:
        """Return a loaded plugin by name.

        Args:
            name: The plugin name.

        Returns:
            The plugin instance, or None if not loaded.
        """
        return self._plugins.get(name)

    def list_plugins(self) -> list[dict[str, str]]:
        """Return metadata for all loaded plugins.

        Returns:
            A list of dicts with name, version, description, and status.
        """
        result = []
        for name, plugin in self._plugins.items():
            result.append({
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "status": "disabled" if name in self._disabled else "active",
            })
        return result

    def dispatch_packet(self, packet: "Packet") -> None:
        """Dispatch a packet to all active plugins for analysis.

        Plugin exceptions are caught and the plugin is disabled.

        Args:
            packet: The dissected packet to dispatch.
        """
        for name, plugin in self._plugins.items():
            if name in self._disabled:
                continue
            try:
                plugin.analyze_packet(packet)
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "plugin_error",
                    plugin=name,
                    error=str(exc),
                    exc_info=True,
                )
                self._disabled.add(name)
                logger.warning("plugin_disabled", plugin=name, reason="unhandled_exception")
