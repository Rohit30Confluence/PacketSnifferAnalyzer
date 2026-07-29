"""CLI: dashboard command group."""

from __future__ import annotations

import click


@click.group(name="dashboard")
def dashboard() -> None:
    """Manage the web dashboard.

    The dashboard is served on localhost only by default.
    """


@dashboard.command(name="start")
@click.option(
    "--host",
    default="127.0.0.1",
    show_default=True,
    help="Host to bind the dashboard to. Default: 127.0.0.1 (localhost only).",
)
@click.option(
    "--port", "-p",
    default=8080,
    show_default=True,
    help="Port for the dashboard.",
)
@click.option(
    "--no-browser",
    is_flag=True,
    default=False,
    help="Do not open the browser automatically.",
)
def dashboard_start(host: str, port: int, no_browser: bool) -> None:
    """Start the web dashboard server.

    \b
    WARNING: Changing --host from 127.0.0.1 exposes the dashboard
    to the network. Only do this if you have appropriate controls.

    \b
    Examples:
        psa dashboard start
        psa dashboard start --port 9090
        psa dashboard start --no-browser
    """
    if host not in ("127.0.0.1", "::1", "localhost"):
        click.echo(
            click.style(
                f"WARNING: Dashboard will be accessible on {host}:{port}. "
                "Ensure you have appropriate network controls.",
                fg="yellow",
            ),
            err=True,
        )

    click.echo("Dashboard will be available in Phase 3 (M5).")


@dashboard.command(name="stop")
def dashboard_stop() -> None:
    """Stop the web dashboard server."""
    click.echo("Dashboard stop will be available in Phase 3 (M5).")
