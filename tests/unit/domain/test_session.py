"""Unit tests for the CaptureSession domain model."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from packetanalyzer.domain.session import CaptureSession, SessionState


@pytest.mark.unit
class TestCaptureSession:
    """Tests for the CaptureSession domain model."""

    def test_session_creation(self, sample_session: CaptureSession) -> None:
        """Session can be created with required fields."""
        assert sample_session.session_id == "test-session-001"
        assert sample_session.interface == "eth0"
        assert sample_session.state == SessionState.RUNNING

    def test_session_is_active_when_running(self, sample_session: CaptureSession) -> None:
        """is_active returns True when state is RUNNING."""
        assert sample_session.is_active is True

    def test_session_is_active_when_paused(self, sample_session: CaptureSession) -> None:
        """is_active returns True when state is PAUSED."""
        sample_session.state = SessionState.PAUSED
        assert sample_session.is_active is True

    def test_session_is_not_active_when_stopped(self, sample_session: CaptureSession) -> None:
        """is_active returns False when state is STOPPED."""
        sample_session.state = SessionState.STOPPED
        assert sample_session.is_active is False

    def test_duration_returns_none_when_running(self, sample_session: CaptureSession) -> None:
        """duration_seconds returns None when session has not stopped."""
        assert sample_session.duration_seconds is None

    def test_duration_returns_seconds_when_stopped(self, sample_session: CaptureSession) -> None:
        """duration_seconds returns the correct duration after stopping."""
        sample_session.stopped_at = datetime(2024, 1, 15, 10, 5, 0, tzinfo=timezone.utc)
        assert sample_session.duration_seconds == 300.0  # 5 minutes
