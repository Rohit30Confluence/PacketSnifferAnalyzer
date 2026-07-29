"""Integration test: StartCapture use case."""

from __future__ import annotations

from unittest.mock import MagicMock, call

import pytest

from packetanalyzer.use_cases.start_capture import StartCaptureUseCase


@pytest.mark.integration
class TestStartCaptureUseCase:
    """Integration tests for the StartCapture use case."""

    def test_start_capture_calls_storage_open(self, mock_capture_port: MagicMock,
                                               mock_storage_port: MagicMock,
                                               mock_audit_logger: MagicMock,
                                               sample_session: object) -> None:
        """StartCapture opens storage before starting capture."""
        use_case = StartCaptureUseCase(
            capture_port=mock_capture_port,
            storage_port=mock_storage_port,
            audit_logger=mock_audit_logger,
        )
        callback = MagicMock()
        use_case.execute(sample_session, callback)  # type: ignore[arg-type]

        mock_storage_port.open_session.assert_called_once_with(sample_session)

    def test_start_capture_calls_capture_start(self, mock_capture_port: MagicMock,
                                                mock_storage_port: MagicMock,
                                                mock_audit_logger: MagicMock,
                                                sample_session: object) -> None:
        """StartCapture starts the capture backend."""
        use_case = StartCaptureUseCase(
            capture_port=mock_capture_port,
            storage_port=mock_storage_port,
            audit_logger=mock_audit_logger,
        )
        callback = MagicMock()
        use_case.execute(sample_session, callback)  # type: ignore[arg-type]

        mock_capture_port.start.assert_called_once()

    def test_start_capture_writes_audit_log(self, mock_capture_port: MagicMock,
                                             mock_storage_port: MagicMock,
                                             mock_audit_logger: MagicMock,
                                             sample_session: object) -> None:
        """StartCapture writes an audit log entry."""
        use_case = StartCaptureUseCase(
            capture_port=mock_capture_port,
            storage_port=mock_storage_port,
            audit_logger=mock_audit_logger,
        )
        callback = MagicMock()
        use_case.execute(sample_session, callback)  # type: ignore[arg-type]

        mock_audit_logger.log_session_start.assert_called_once_with(sample_session)
