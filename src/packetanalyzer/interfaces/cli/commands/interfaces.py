"""CLI: network interface discovery."""

from __future__ import annotations

import json

import click

from packetanalyzer.infrastructure.privilege import check_privileges


@click.command(name="interfaces")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Output interface information as JSON.",
)
def interfaces(output_json: bool) -> None:
    """List network interfaces available to PacketSnifferAnalyzer."""

    privilege = check_privileges()

    if not privilege.has_sufficient_privileges:
        click.echo(
            click.style("ERROR: Insufficient privileges.", fg="red"),
            err=True,
        )
        click.echo(privilege.remediation, err=True)
        raise click.exceptions.Exit(1)


    adapter = ScapyCaptureAdapter()
    discovered = adapter.list_interfaces()

    if output_json:
        click.echo(
            json.dumps(
                [
                    {
                        "name": item.name,
                        "description": item.description,
                        "is_up": item.is_up,
                        "is_loopback": item.is_loopback,
                        "addresses": item.addresses,
                    }
                    for item in discovered
                ],
                indent=2,
            )
        )
        return

    if not discovered:
        click.echo("No network interfaces found.")
        return

    for item in discovered:
        state = "UP" if item.is_up else "DOWN"
        loopback = " LOOPBACK" if item.is_loopback else ""
        addresses = ", ".join(item.addresses) or "-"
        click.echo(
            f"{item.name:<12} {state:<4}{loopback:<10} "
            f"{addresses}"
        )
