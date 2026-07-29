"""CLI: interfaces command — list available network interfaces."""

from __future__ import annotations

import click


@click.command(name="interfaces")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Output as JSON.",
)
def interfaces(output_json: bool) -> None:
    """List all available network interfaces on this host.

    Displays interface name, status, and IP addresses.
    Requires sufficient privileges on some platforms.

    \b
    Examples:
        psa interfaces
        psa interfaces --json
    """
    from packetanalyzer.infrastructure.privilege import check_privileges

    status = check_privileges()
    if not status.has_sufficient_privileges:
        click.echo(
            click.style("ERROR: Insufficient privileges.", fg="red"),
            err=True,
        )
        click.echo(status.remediation, err=True)
        raise SystemExit(1)

    # Implementation: calls ScapyCaptureAdapter.list_interfaces()
    # Full implementation in Phase 3 — M1
    click.echo("Interface listing will be available in Phase 3 (M1).")
