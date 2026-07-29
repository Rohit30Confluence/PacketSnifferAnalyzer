"""CLI application root.

Defines the top-level Click command group and registers all sub-commands.
"""

from __future__ import annotations

import click

from packetanalyzer import __version__


@click.group()
@click.version_option(version=__version__, prog_name="psa")
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Enable debug logging.",
)
@click.pass_context
def cli(ctx: click.Context, debug: bool) -> None:
    """PacketSnifferAnalyzer — Network packet capture and analysis tool.

    \b
    LEGAL NOTICE: Packet capture on a network you do not own or have
    explicit written authorization to monitor may violate applicable laws.
    You are solely responsible for compliance with applicable laws.

    Run 'psa COMMAND --help' for help on a specific command.
    """
    ctx.ensure_object(dict)
    ctx.obj["debug"] = debug

    from packetanalyzer.infrastructure.config import get_settings
    from packetanalyzer.infrastructure.logging import configure_logging

    settings = get_settings()
    configure_logging(
        log_level="DEBUG" if debug else settings.log_level,
        log_dir=settings.log_dir,
        json_output=not debug,
    )


# Register sub-command groups
from packetanalyzer.interfaces.cli.commands.capture import capture  # noqa: E402
from packetanalyzer.interfaces.cli.commands.analyze import analyze  # noqa: E402
from packetanalyzer.interfaces.cli.commands.export import export  # noqa: E402
from packetanalyzer.interfaces.cli.commands.dashboard import dashboard  # noqa: E402
from packetanalyzer.interfaces.cli.commands.interfaces import interfaces  # noqa: E402

cli.add_command(capture)
cli.add_command(analyze)
cli.add_command(export)
cli.add_command(dashboard)
cli.add_command(interfaces)
