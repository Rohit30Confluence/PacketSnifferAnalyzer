"""Unit tests for the AuditLogger."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from packetanalyzer.infrastructure.audit import AuditLogger


@pytest.mark.unit
class TestAuditLogger:
    """Tests for the AuditLogger."""

    def test_audit_logger_creates_log_file(self, tmp_path: Path) -> None:
        """AuditLogger creates the log file and parent directories."""
        log_path = tmp_path / "audit" / "audit.log"
        logger = AuditLogger(log_path)
        logger.log_legal_notice_accepted()
        assert log_path.exists()

    def test_audit_log_entry_is_valid_json(self, tmp_path: Path) -> None:
        """Each audit log entry is valid JSON."""
        log_path = tmp_path / "audit.log"
        logger = AuditLogger(log_path)
        logger.log_legal_notice_accepted()

        lines = log_path.read_text().strip().splitlines()
        assert len(lines) == 1
        entry = json.loads(lines[0])
        assert entry["event_type"] == "legal_notice_accepted"
        assert "timestamp" in entry
        assert "operator" in entry

    def test_audit_log_session_start(self, tmp_path: Path, sample_session: object) -> None:
        """log_session_start writes a session_start event."""
        log_path = tmp_path / "audit.log"
        logger = AuditLogger(log_path)
        logger.log_session_start(sample_session)  # type: ignore[arg-type]

        entry = json.loads(log_path.read_text().strip())
        assert entry["event_type"] == "session_start"
        assert entry["session_id"] == "test-session-001"
        assert entry["interface"] == "eth0"

    def test_audit_log_appends_entries(self, tmp_path: Path) -> None:
        """Multiple log calls append entries rather than overwriting."""
        log_path = tmp_path / "audit.log"
        logger = AuditLogger(log_path)
        logger.log_legal_notice_accepted()
        logger.log_legal_notice_accepted()

        lines = log_path.read_text().strip().splitlines()
        assert len(lines) == 2

    def test_audit_log_does_not_contain_payload(self, tmp_path: Path, sample_session: object) -> None:
        """Audit log entries never contain packet payload data."""
        log_path = tmp_path / "audit.log"
        logger = AuditLogger(log_path)
        logger.log_session_start(sample_session)  # type: ignore[arg-type]

        content = log_path.read_text()
        # Verify no raw bytes or payload-like content
        assert "raw_bytes" not in content
        assert "payload" not in content
