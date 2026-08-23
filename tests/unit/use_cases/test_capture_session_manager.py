"""Unit tests for the capture-session application coordinator."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from packetanalyzer.domain.session import CaptureSession, SessionState
from packetanalyzer.use_cases.capture_session_manager import (
    CaptureSessionManager,
)


def make_session(
    *,
    session_id: str = "session-001",
    state: SessionState = SessionState.CREATED,
) -> CaptureSession:
    return CaptureSession(
        session_id=session_id,
        name="Test Capture",
        interface="en0",
        bpf_filter="tcp",
        started_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        state=state,
        operator="tester",
        tool_version="test",
    )


@pytest.fixture
def capture() -> MagicMock:
    return MagicMock()


@pytest.fixture
def storage() -> MagicMock:
    return MagicMock()


@pytest.fixture
def audit() -> MagicMock:
    return MagicMock()


@pytest.fixture
def manager(
    capture: MagicMock,
    storage: MagicMock,
    audit: MagicMock,
) -> CaptureSessionManager:
    return CaptureSessionManager(
        capture_port=capture,
        storage_port=storage,
        audit_logger=audit,
    )


def test_start_creates_active_session(
    manager: CaptureSessionManager,
    capture: MagicMock,
    storage: MagicMock,
    audit: MagicMock,
) -> None:
    session = make_session()
    callback = MagicMock()

    result = manager.start(session, callback)

    assert result is session
    assert manager.active_session is session
    assert session.state == SessionState.RUNNING
    storage.open_session.assert_called_once_with(session)
    capture.start.assert_called_once_with(session, callback)
    audit.log_session_start.assert_called_once_with(session)


def test_start_rejects_second_active_session(
    manager: CaptureSessionManager,
) -> None:
    first = make_session(session_id="first")
    second = make_session(session_id="second")

    manager.start(first, MagicMock())

    with pytest.raises(RuntimeError, match="already active"):
        manager.start(second, MagicMock())


def test_start_rolls_back_manager_state_when_backend_fails(
    manager: CaptureSessionManager,
    capture: MagicMock,
) -> None:
    session = make_session()
    capture.start.side_effect = RuntimeError("capture failed")

    with pytest.raises(RuntimeError, match="capture failed"):
        manager.start(session, MagicMock())

    assert manager.active_session is None
    assert session.state == SessionState.ERROR


def test_stop_stops_backend_and_clears_active_session(
    manager: CaptureSessionManager,
    capture: MagicMock,
    storage: MagicMock,
    audit: MagicMock,
) -> None:
    session = make_session()
    manager.start(session, MagicMock())

    manager.stop()

    capture.stop.assert_called_once()
    storage.close_session.assert_called_once_with(session)
    audit.log_session_stop.assert_called_once_with(session)
    assert manager.active_session is None
    assert session.state == SessionState.STOPPED


def test_stop_without_active_session_fails(
    manager: CaptureSessionManager,
) -> None:
    with pytest.raises(RuntimeError, match="No active capture"):
        manager.stop()


def test_pause_delegates_and_preserves_active_session(
    manager: CaptureSessionManager,
    capture: MagicMock,
) -> None:
    session = make_session()
    manager.start(session, MagicMock())

    manager.pause()

    capture.pause.assert_called_once()
    assert manager.active_session is session
    assert session.state == SessionState.PAUSED


def test_pause_without_active_session_fails(
    manager: CaptureSessionManager,
) -> None:
    with pytest.raises(RuntimeError, match="No active capture"):
        manager.pause()


def test_resume_delegates_and_preserves_active_session(
    manager: CaptureSessionManager,
    capture: MagicMock,
) -> None:
    session = make_session()
    manager.start(session, MagicMock())
    manager.pause()

    manager.resume()

    capture.resume.assert_called_once()
    assert manager.active_session is session
    assert session.state == SessionState.RUNNING


def test_resume_without_active_session_fails(
    manager: CaptureSessionManager,
) -> None:
    with pytest.raises(RuntimeError, match="No active capture"):
        manager.resume()


def test_status_returns_active_session(
    manager: CaptureSessionManager,
) -> None:
    session = make_session()
    manager.start(session, MagicMock())

    assert manager.status() is session


def test_status_returns_none_when_idle(
    manager: CaptureSessionManager,
) -> None:
    assert manager.status() is None


def test_refresh_statistics_updates_drop_count(
    manager: CaptureSessionManager,
    capture: MagicMock,
) -> None:
    session = make_session()
    manager.start(session, MagicMock())
    capture.get_drop_count.return_value = 7

    manager.refresh_statistics()

    assert session.drop_count == 7


def test_refresh_statistics_without_active_session_is_noop(
    manager: CaptureSessionManager,
    capture: MagicMock,
) -> None:
    manager.refresh_statistics()

    capture.get_drop_count.assert_not_called()


def test_stop_clears_manager_even_if_storage_close_fails(
    manager: CaptureSessionManager,
    storage: MagicMock,
) -> None:
    session = make_session()
    manager.start(session, MagicMock())
    storage.close_session.side_effect = RuntimeError("close failed")

    with pytest.raises(RuntimeError, match="close failed"):
        manager.stop()

    assert manager.active_session is None
    assert session.state == SessionState.STOPPED
