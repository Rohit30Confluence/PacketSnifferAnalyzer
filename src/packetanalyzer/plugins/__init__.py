"""Plugin system for PacketSnifferAnalyzer.

The plugin system allows third-party dissectors and analysis modules
to be loaded at runtime without modifying core code.

Plugin contract:
    All plugins must implement the PluginInterface abstract base class.
    Plugins are discovered from the plugins/ directory at startup.
    Plugin errors are isolated — a failing plugin cannot crash the core engine.

Security:
    Only load plugins from sources you trust. Plugins have access to
    dissected packet data. Plugin signature verification is on the roadmap.
"""
