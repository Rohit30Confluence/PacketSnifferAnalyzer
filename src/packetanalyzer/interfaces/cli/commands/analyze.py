"""CLI: analyze command — offline PCAP analysis."""

from __future__ import annotations

import click


@click.command(name="analyze")
@click.option(
    "--file", "-f", "pcap_file",
    required=True,
    type=click.Path(exists=True, readable=True, dir_okay=False),
    help="Path to the PCAP file to analyze.",
)
@click.option(
    "--filter", "display_filter",
    default="",
    help="Display filter expression.",
)
@click.option(
    "--stats",
    is_flag=True,
    default=False,
    help="Show traffic statistics summary.",
)
@click.option(
    "--flows",
    is_flag=True,
    default=False,
    help="Show flow table.",
)
def analyze(
    pcap_file: str,
    display_filter: str,
    stats: bool,
    flows: bool,
) -> None:
    """Analyze an existing PCAP file.

    \b
    Examples:
        psa analyze --file capture.pcap
        psa analyze -f capture.pcap --filter "ip.src == 192.168.1.1"
        psa analyze -f capture.pcap --stats --flows
    """
    click.echo("Offline analysis will be available in Phase 3 (M1).")
