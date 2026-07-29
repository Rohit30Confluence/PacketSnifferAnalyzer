"""CLI output formatters.

Provides consistent formatting for CLI output across all commands.
"""

from __future__ import annotations

import json
from typing import Any

import click


def format_table(headers: list[str], rows: list[list[Any]], widths: list[int] | None = None) -> str:
    """Format data as a plain-text table.

    Args:
        headers: Column header names.
        rows: Data rows, each a list of values.
        widths: Optional column widths. Auto-calculated if not provided.

    Returns:
        A formatted table string.
    """
    if widths is None:
        widths = [max(len(str(h)), max((len(str(r[i])) for r in rows), default=0))
                  for i, h in enumerate(headers)]

    separator = "-+-".join("-" * w for w in widths)
    header_row = " | ".join(str(h).ljust(w) for h, w in zip(headers, widths))

    lines = [header_row, separator]
    for row in rows:
        lines.append(" | ".join(str(v).ljust(w) for v, w in zip(row, widths)))

    return "\n".join(lines)


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as pretty-printed JSON.

    Args:
        data: The data to serialize.
        indent: JSON indentation level.

    Returns:
        A JSON string.
    """
    return json.dumps(data, indent=indent, default=str)


def print_error(message: str) -> None:
    """Print an error message to stderr in red.

    Args:
        message: The error message.
    """
    click.echo(click.style(f"ERROR: {message}", fg="red"), err=True)


def print_warning(message: str) -> None:
    """Print a warning message to stderr in yellow.

    Args:
        message: The warning message.
    """
    click.echo(click.style(f"WARNING: {message}", fg="yellow"), err=True)


def print_success(message: str) -> None:
    """Print a success message in green.

    Args:
        message: The success message.
    """
    click.echo(click.style(f"OK: {message}", fg="green"))
