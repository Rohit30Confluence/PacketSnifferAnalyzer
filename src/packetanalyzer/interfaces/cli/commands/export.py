"""CLI: export command."""

from __future__ import annotations

import click


@click.command(name="export")
@click.option(
    "--session", "-s",
    required=True,
    help="Session ID or name to export.",
)
@click.option(
    "--format", "-f", "fmt",
    type=click.Choice(["pcap", "json", "csv", "text"], case_sensitive=False),
    default="pcap",
    show_default=True,
    help="Export format.",
)
@click.option(
    "--output", "-o",
    required=True,
    help="Output file path.",
)
@click.option(
    "--filter", "display_filter",
    default="",
    help="Export only packets matching this filter.",
)
@click.option(
    "--redact-payload",
    is_flag=True,
    default=False,
    help="Replace payload bytes with zeros in the export.",
)
def export(
    session: str,
    fmt: str,
    output: str,
    display_filter: str,
    redact_payload: bool,
) -> None:
    """Export a capture session to a file.

    \b
    Examples:
        psa export --session my-session --format json --output results.json
        psa export -s abc123 -f csv -o traffic.csv
        psa export -s abc123 -f json -o results.json --redact-payload
    """
    click.echo("Export will be available in Phase 3 (M3).")
