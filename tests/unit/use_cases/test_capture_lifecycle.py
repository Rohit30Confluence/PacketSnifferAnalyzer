"""Regression tests for capture lifecycle use cases."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from packetanalyzer.domain.session import CaptureSession
from packetanalyzer.use_cases.start_capture import StartCaptureUseCase
from packetanalyzer.use_cases.stop_capture import StopCaptureUseCase


def make_session() -> CaptureSession:
    """Create a deterministic session for lifecycle tests."""
    return CaptureSession(
        session_id="lifecycle-test",
        name="Lifecycle Test",
        interface="en0",
    )


class TestStartCaptureUseCase:
    """Regression tests for capture startup."""

    def make_use_case(
        self,
    ) -> tuple[
        StartCaptureUseCase,
        MagicMock,
        MagicMock,
        MagicMock,
    ]:
        capture = MagicMock()
        storage = MagicMock()
        audit = MagicMock()

        use_case = StartCaptureUseCase(
            capture_port=capture,
            storage_port=storage,
            audit_logger=audit,
        )

        return use_case, capture, storage, audit

    def test_successful_start_has_strict_order(self) -> None:
        """Storage opens before capture and audit comes last."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()
        callback = MagicMock()

        events: list[str] = []

        storage.open_session.side_effect = (
            lambda _session: events.append("storage.open")
        )
        capture.start.side_effect = (
            lambda _session, _callback: events.append("capture.start")
        )
        audit.log_session_start.side_effect = (
            lambda _session: events.append("audit.start")
        )

        use_case.execute(session, callback)

        assert events == [
            "storage.open",
            "capture.start",
            "audit.start",
        ]

    def test_storage_failure_prevents_later_steps(self) -> None:
        """Storage failure prevents capture and audit."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        storage.open_session.side_effect = RuntimeError("storage failed")

        with pytest.raises(RuntimeError, match="storage failed"):
            use_case.execute(session, MagicMock())

        capture.start.assert_not_called()
        capture.stop.assert_not_called()
        audit.log_session_start.assert_not_called()
        storage.close_session.assert_not_called()

    def test_capture_failure_rolls_back_storage(self) -> None:
        """Capture failure closes storage that was already opened."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        capture.start.side_effect = RuntimeError("capture failed")

        with pytest.raises(RuntimeError, match="capture failed"):
            use_case.execute(session, MagicMock())

        storage.open_session.assert_called_once_with(session)
        storage.close_session.assert_called_once_with(session)
        capture.stop.assert_not_called()
        audit.log_session_start.assert_not_called()

    def test_capture_failure_preserves_original_exception(self) -> None:
        """Storage cleanup failure cannot hide capture startup failure."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        capture.start.side_effect = RuntimeError("capture failed")
        storage.close_session.side_effect = RuntimeError("cleanup failed")

        with pytest.raises(RuntimeError, match="capture failed"):
            use_case.execute(session, MagicMock())

        capture.stop.assert_not_called()
        audit.log_session_start.assert_not_called()

    def test_audit_failure_rolls_back_capture_and_storage(self) -> None:
        """Audit failure after startup rolls back both resources."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        audit.log_session_start.side_effect = RuntimeError("audit failed")

        with pytest.raises(RuntimeError, match="audit failed"):
            use_case.execute(session, MagicMock())

        capture.stop.assert_called_once_with()
        storage.close_session.assert_called_once_with(session)

    def test_audit_failure_preserves_original_exception(self) -> None:
        """Cleanup failures cannot hide the audit failure."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        audit.log_session_start.side_effect = RuntimeError("audit failed")
        capture.stop.side_effect = RuntimeError("stop cleanup failed")
        storage.close_session.side_effect = RuntimeError("close cleanup failed")

        with pytest.raises(RuntimeError, match="audit failed"):
            use_case.execute(session, MagicMock())

        capture.stop.assert_called_once_with()
        storage.close_session.assert_called_once_with(session)

    def test_successful_start_calls_dependencies_once(self) -> None:
        """Successful startup invokes each dependency exactly once."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()
        callback = MagicMock()

        use_case.execute(session, callback)

        storage.open_session.assert_called_once_with(session)
        capture.start.assert_called_once_with(session, callback)
        audit.log_session_start.assert_called_once_with(session)
        capture.stop.assert_not_called()
        storage.close_session.assert_not_called()


class TestStopCaptureUseCase:
    """Regression tests for capture shutdown."""

    def make_use_case(
        self,
    ) -> tuple[
        StopCaptureUseCase,
        MagicMock,
        MagicMock,
        MagicMock,
    ]:
        capture = MagicMock()
        storage = MagicMock()
        audit = MagicMock()

        use_case = StopCaptureUseCase(
            capture_port=capture,
            storage_port=storage,
            audit_logger=audit,
        )

        return use_case, capture, storage, audit

    def test_successful_stop_has_strict_order(self) -> None:
        """Capture stops before storage closes and audit comes last."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        events: list[str] = []

        capture.stop.side_effect = lambda: events.append("capture.stop")
        storage.close_session.side_effect = (
            lambda _session: events.append("storage.close")
        )
        audit.log_session_stop.side_effect = (
            lambda _session: events.append("audit.stop")
        )

        use_case.execute(session)

        assert events == [
            "capture.stop",
            "storage.close",
            "audit.stop",
        ]

    def test_capture_stop_failure_prevents_later_steps(self) -> None:
        """Capture shutdown failure prevents storage and audit."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        capture.stop.side_effect = RuntimeError("stop failed")

        with pytest.raises(RuntimeError, match="stop failed"):
            use_case.execute(session)

        storage.close_session.assert_not_called()
        audit.log_session_stop.assert_not_called()

    def test_storage_close_failure_prevents_final_audit(self) -> None:
        """Storage failure prevents a false successful-stop audit."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        storage.close_session.side_effect = RuntimeError("close failed")

        with pytest.raises(RuntimeError, match="close failed"):
            use_case.execute(session)

        capture.stop.assert_called_once_with()
        audit.log_session_stop.assert_not_called()

    def test_audit_failure_does_not_repeat_shutdown(self) -> None:
        """Audit failure does not cause shutdown operations to repeat."""
        use_case, capture, storage, audit = self.make_use_case()
        session = make_session()

        audit.log_session_stop.side_effect = RuntimeError("audit failed")

        with pytest.raises(RuntimeError, match="audit failed"):
            use_case.execute(session)

        capture.stop.assert_called_once_with()
        storage.close_session.assert_called_once_with(session)
        audit.log_session_stop.assert_called_once_with(session)
