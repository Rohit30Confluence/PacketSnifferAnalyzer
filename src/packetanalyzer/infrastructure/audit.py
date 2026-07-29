"""Append-only audit logger.

The audit logger records security-relevant events in a structured,
append-only log file. It is separate from the application log and
must never contain packet payload data.

Audit events include:
- Session start and stop
- Filter changes
- Export actions
- Alert triggers
- First-run legal notice acceptance
"""

from __future__ import annotations

import getpass
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from packetanalyzer.domain.session import CaptureSession
    from packetanalyzer.domain.alert import AlertEvent


class AuditLogger:
    """Writes structured audit events to an append-only log file.

    The audit log is written in newline-delimited JSON (NDJSON) format.
    Each line is a self-contained JSON object with a timestamp, event
    type, and event-specific fields.

    Args:
        log_path: Path to the audit log file.
    """

    def __init__(self, log_path: Path) -> None:
        self._log_path = log_path
        self._log_path.parent.mkdir(parents=True, exist_ok=True)
        self._operator = self._get_operator()

    def _get_operator(self) -> str:
        """Return the current OS username."""
        try:
            return getpass.getuser()
        except Exception:  # noqa: BLE001
            return "unknown"

    def _write(self, event_type: str, fields: dict[str, Any]) -> None:
        """Write a single audit event to the log file.

        Args:
            event_type: The type of audit event.
            fields: Event-specific fields to include.
        """
        entry = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "event_type": event_type,
            "operator": self._operator,
            "pid": os.getpid(),
            **fields,
        }
        with self._log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def log_session_start(self, session: "CaptureSession") -> None:
        """Log a session start event.

        Args:
            session: The session that was started.
        """
        self._write(
            "session_start",
            {
                "session_id": session.session_id,
                "session_name": session.name,
                "interface": session.interface,
                "bpf_filter": session.bpf_filter,
                "tool_version": session.tool_version,
            },
        )

    def log_session_stop(self, session: "CaptureSession") -> None:
        """Log a session stop event.

        Args:
            session: The session that was stopped.
        """
        self._write(
            "session_stop",
            {
                "session_id": session.session_id,
                "packet_count": session.packet_count,
                "byte_count": session.byte_count,
                "drop_count": session.drop_count,
                "duration_seconds": session.duration_seconds,
            },
        )

    def log_export(self, session_id: str, fmt: str, output_path: str, packet_count: int) -> None:
        """Log an export action.

        Args:
            session_id: The session that was exported.
            fmt: The export format used.
            output_path: The file path written to.
            packet_count: The number of packets exported.
        """
        self._write(
            "export",
            {
                "session_id": session_id,
                "format": fmt,
                "output_path": output_path,
                "packet_count": packet_count,
            },
        )

    def log_alert_triggered(self, event: "AlertEvent") -> None:
        """Log an alert trigger event.

        Args:
            event: The alert event that was triggered.
        """
        self._write(
            "alert_triggered",
            {
                "event_id": event.event_id,
                "rule_id": event.rule.rule_id,
                "rule_name": event.rule.name,
                "severity": event.rule.severity.name,
                "observed_value": event.observed_value,
                "threshold": event.rule.threshold,
            },
        )

    def log_legal_notice_accepted(self) -> None:
        """Log that the user accepted the legal notice on first run."""
        self._write("legal_notice_accepted", {})
