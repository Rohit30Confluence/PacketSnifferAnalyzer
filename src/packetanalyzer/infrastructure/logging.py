"""Structured logging configuration using structlog.

All application logging must go through this module. Direct use of
the stdlib logging module is discouraged in application code.

Usage:
    from packetanalyzer.infrastructure.logging import get_logger

    logger = get_logger(__name__)
    logger.info("capture_started", interface="eth0", session_id="abc123")
"""

from __future__ import annotations

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Any

import structlog

_CONFIGURED = False


def configure_logging(
    log_level: str = "INFO",
    log_dir: Path | None = None,
    json_output: bool = True,
) -> None:
    """Configure structlog and stdlib logging for the application.

    This function is idempotent — calling it multiple times has no effect
    after the first call.

    Args:
        log_level: The minimum log level to emit (DEBUG, INFO, WARNING, ERROR).
        log_dir: Directory for log files. If None, logs to stderr only.
        json_output: If True, emit JSON-formatted log lines. If False,
            emit human-readable colored output (for development).
    """
    global _CONFIGURED  # noqa: PLW0603
    if _CONFIGURED:
        return

    level = getattr(logging, log_level.upper(), logging.INFO)

    handlers: list[logging.Handler] = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    handlers.append(console_handler)

    # File handlers (if log_dir provided)
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)

        app_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=30,
            encoding="utf-8",
        )
        app_handler.setLevel(level)
        handlers.append(app_handler)

        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / "error.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=30,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.ERROR)
        handlers.append(error_handler)

    logging.basicConfig(
        level=level,
        handlers=handlers,
        format="%(message)s",
    )

    processors: list[Any] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.ExceptionRenderer(),
    ]

    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    _CONFIGURED = True


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a bound structlog logger for the given module name.

    Args:
        name: Typically __name__ of the calling module.

    Returns:
        A structlog BoundLogger instance.
    """
    return structlog.get_logger(name)  # type: ignore[return-value]
