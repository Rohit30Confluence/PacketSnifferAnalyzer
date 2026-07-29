"""PacketSnifferAnalyzer — Application entry point.

This module provides the top-level entry point for the application.
It delegates to the CLI adapter, which handles command routing.
"""

from __future__ import annotations


def main() -> None:
    """Entry point for the `psa` command-line tool."""
    from packetanalyzer.interfaces.cli.app import cli

    cli()


if __name__ == "__main__":
    main()
