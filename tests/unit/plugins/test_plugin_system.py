"""Unit tests for the plugin system."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from packetanalyzer.plugins.interface import PluginInterface
from packetanalyzer.plugins.manager import PluginManager
from packetanalyzer.plugins.examples.http_path_logger import HttpPathLoggerPlugin


@pytest.mark.unit
class TestPluginInterface:
    """Tests for the PluginInterface contract."""

    def test_example_plugin_implements_interface(self) -> None:
        """HttpPathLoggerPlugin correctly implements PluginInterface."""
        plugin = HttpPathLoggerPlugin()
        assert isinstance(plugin, PluginInterface)

    def test_example_plugin_has_required_properties(self) -> None:
        """Example plugin has name, version, and description."""
        plugin = HttpPathLoggerPlugin()
        assert plugin.name == "http_path_logger"
        assert plugin.version == "1.0.0"
        assert len(plugin.description) > 0

    def test_example_plugin_protocols_is_list(self) -> None:
        """plugins.protocols returns a list."""
        plugin = HttpPathLoggerPlugin()
        assert isinstance(plugin.protocols, list)


@pytest.mark.unit
class TestPluginManager:
    """Tests for the PluginManager."""

    def test_plugin_manager_initializes_empty(self, tmp_path: Path) -> None:
        """PluginManager starts with no loaded plugins."""
        manager = PluginManager(tmp_path)
        assert manager.list_plugins() == []

    def test_dispatch_packet_to_failing_plugin_disables_it(
        self, tmp_path: Path, sample_packet: object
    ) -> None:
        """A plugin that raises an exception is disabled, not crashed."""
        manager = PluginManager(tmp_path)

        # Manually inject a failing plugin
        failing_plugin = MagicMock(spec=PluginInterface)
        failing_plugin.name = "failing_plugin"
        failing_plugin.analyze_packet.side_effect = RuntimeError("Plugin crashed")
        manager._plugins["failing_plugin"] = failing_plugin

        # Should not raise
        manager.dispatch_packet(sample_packet)  # type: ignore[arg-type]

        # Plugin should be disabled
        assert "failing_plugin" in manager._disabled

    def test_dispatch_packet_skips_disabled_plugins(
        self, tmp_path: Path, sample_packet: object
    ) -> None:
        """Disabled plugins are not called during dispatch."""
        manager = PluginManager(tmp_path)

        plugin = MagicMock(spec=PluginInterface)
        plugin.name = "test_plugin"
        manager._plugins["test_plugin"] = plugin
        manager._disabled.add("test_plugin")

        manager.dispatch_packet(sample_packet)  # type: ignore[arg-type]

        plugin.analyze_packet.assert_not_called()
