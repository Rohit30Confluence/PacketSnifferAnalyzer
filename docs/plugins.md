# Plugin Development Guide

This guide explains how to write custom dissectors and analysis plugins for PacketSnifferAnalyzer.

---

## Overview

The plugin system allows you to extend PacketSnifferAnalyzer without modifying core code. Plugins can:

- Add custom protocol dissectors
- Perform post-dissection packet analysis
- Generate custom statistics or alerts
- Export data to custom formats

---

## Plugin Contract

All plugins must implement the `PluginInterface` abstract base class from `packetanalyzer.plugins.interface`.

### Required Properties

| Property | Type | Description |
|---|---|---|
| `name` | `str` | Unique plugin identifier (snake_case) |
| `version` | `str` | SemVer version string |
| `description` | `str` | Brief description of the plugin |

### Optional Properties and Methods

| Member | Description |
|---|---|
| `protocols` | List of protocol names this plugin dissects |
| `on_load()` | Called when the plugin is loaded |
| `on_unload()` | Called when the plugin is unloaded |
| `dissect_layer(protocol, raw)` | Dissect a protocol layer from raw bytes |
| `analyze_packet(packet)` | Analyze a fully dissected packet |

---

## Creating a Plugin

### Step 1: Create the Plugin Directory

```
plugins/
  my_plugin/
    __init__.py
    README.md
```

### Step 2: Implement PluginInterface

```python
# plugins/my_plugin/__init__.py
from __future__ import annotations
from packetanalyzer.plugins.interface import PluginInterface
from packetanalyzer.infrastructure.logging import get_logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from packetanalyzer.domain.packet import Packet

logger = get_logger(__name__)


class MyPlugin(PluginInterface):
    @property
    def name(self) -> str:
        return "my_plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "A brief description of what my plugin does."

    def on_load(self) -> None:
        logger.info("plugin_loaded", plugin=self.name)

    def analyze_packet(self, packet: "Packet") -> None:
        # Your analysis logic here
        # IMPORTANT: This method must be non-blocking
        # IMPORTANT: Do not log packet payloads
        if packet.has_layer("TCP"):
            tcp = packet.get_layer("TCP")
            if tcp:
                logger.debug("tcp_packet", dport=tcp.get_field("dport"))
```

### Step 3: Place the Plugin

Place your plugin directory in the `plugins/` directory at the project root:

```
PacketSnifferAnalyzer/
  plugins/
    my_plugin/
      __init__.py
```

The plugin manager discovers plugins automatically at startup.

---

## Plugin Rules and Ethical Requirements

All plugins must comply with the [ethical policy](../CONTRIBUTING.md#ethical-policy):

- **Do not** log, store, or transmit packet payload bytes
- **Do not** extract, highlight, or label credentials
- **Do not** transmit data to external servers without explicit user action
- **Do not** perform blocking operations in `analyze_packet()`
- **Do not** modify the `Packet` object passed to `analyze_packet()`

Plugins that violate these rules will be rejected from the official repository.

---

## Error Handling

Plugin errors are isolated. If your plugin raises an unhandled exception:

1. The exception is caught by the plugin manager
2. The error is logged with full stack trace
3. Your plugin is disabled for the remainder of the session
4. The core engine continues without interruption

To prevent your plugin from being disabled, handle all exceptions internally:

```python
def analyze_packet(self, packet: "Packet") -> None:
    try:
        # Your logic
        pass
    except Exception:
        logger.exception("my_plugin_error", plugin=self.name)
        # Do not re-raise
```

---

## Example Plugin

See `src/packetanalyzer/plugins/examples/http_path_logger/` for a complete, documented example plugin.

---

## Plugin Versioning

Use [Semantic Versioning](https://semver.org/) for your plugin version. Breaking changes to the `PluginInterface` will be announced in the changelog with a migration guide.
