"""CLI: capture command group."""

from __future__ import annotations

import click


@click.group(name="capture")
def capture() -> None:
    """Manage packet capture sessions.

    \b
    Sub-commands:
        start   Start a new capture session
        stop    Stop the active capture session
        pause   Pause the active capture session
        resume  Resume a paused capture session
        status  Show current session status
    """


@capture.command(name="start")
@click.option(
    "--interface", "-i",
    required=True,
    help="Network interface to capture on (e.g., eth0, wlan0).",
)
@click.option(
    "--filter", "-f", "bpf_filter",
    default="",
    help="BPF filter expression (e.g., 'tcp port 80').",
)
@click.option(
    "--output", "-o",
    default=None,
    help="Output PCAP file path. Auto-generated if not specified.",
)
@click.option(
    "--name", "-n",
    default=None,
    help="Session name. Auto-generated if not specified.",
)
@click.option(
    "--encrypt",
    is_flag=True,
    default=False,
    help="Encrypt the output PCAP file with AES-256-GCM.",
)
@click.option(
    "--count", "-c",
    default=0,
    help="Stop after capturing this many packets (0 = unlimited).",
)
def capture_start(
    interface: str,
    bpf_filter: str,
    output: str | None,
    name: str | None,
    encrypt: bool,
    count: int,
) -> None:
    """Start a new packet capture session.

    \b
    Examples:
        sudo psa capture start --interface eth0
        sudo psa capture start -i wlan0 -f "tcp port 443"
        sudo psa capture start -i eth0 -f "host 192.168.1.1" -o capture.pcap
        sudo psa capture start -i eth0 --encrypt
    """
    # Full implementation in Phase 3 — M1
    click.echo("Capture start will be available in Phase 3 (M1).")


@capture.command(name="stop")
def capture_stop() -> None:
    """Stop the active capture session."""
    click.echo("Capture stop will be available in Phase 3 (M1).")


@capture.command(name="pause")
def capture_pause() -> None:
    """Pause the active capture session."""
    click.echo("Capture pause will be available in Phase 3 (M1).")


@capture.command(name="resume")
def capture_resume() -> None:
    """Resume a paused capture session."""
    click.echo("Capture resume will be available in Phase 3 (M1).")


@capture.command(name="status")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    default=False,
    help="Output as JSON.",
)
def capture_status(output_json: bool) -> None:
    """Show the status of the active capture session."""
    click.echo("Capture status will be available in Phase 3 (M1).")
