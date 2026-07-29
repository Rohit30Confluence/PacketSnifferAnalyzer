"""Application configuration management.

Configuration is loaded from environment variables and an optional
YAML configuration file. Pydantic Settings is used for validation
and type coercion.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application-wide configuration settings.

    Settings are loaded from environment variables prefixed with PSA_.
    An optional .env file is also supported.

    Attributes:
        env: The runtime environment (development, production).
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR).
        log_dir: Directory for log files.
        data_dir: Directory for session data and PCAP files.
        dashboard_host: Host to bind the web dashboard to.
        dashboard_port: Port for the web dashboard.
        default_snaplen: Default packet snapshot length in bytes.
        ring_buffer_size: Size of the capture ring buffer (packet count).
        pcap_rotation_size_mb: Rotate PCAP files at this size (MB).
        pcap_rotation_interval_hours: Rotate PCAP files at this interval.
        session_flush_interval_seconds: Flush session data to disk interval.
        max_display_packets: Maximum packets to hold in the display queue.
        first_run: Whether this is the first run (legal notice not yet shown).
    """

    model_config = SettingsConfigDict(
        env_prefix="PSA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    env: str = Field(default="production")
    log_level: str = Field(default="INFO")
    log_dir: Path = Field(default=Path.home() / ".packetanalyzer" / "logs")
    data_dir: Path = Field(default=Path.home() / ".packetanalyzer" / "sessions")
    dashboard_host: str = Field(default="127.0.0.1")
    dashboard_port: int = Field(default=8080, ge=1024, le=65535)
    default_snaplen: int = Field(default=65535, ge=64, le=65535)
    ring_buffer_size: int = Field(default=65536, ge=1024)
    pcap_rotation_size_mb: int = Field(default=100, ge=1)
    pcap_rotation_interval_hours: int = Field(default=1, ge=1)
    session_flush_interval_seconds: int = Field(default=5, ge=1)
    max_display_packets: int = Field(default=100_000, ge=1000)
    first_run: bool = Field(default=True)

    @field_validator("dashboard_host")
    @classmethod
    def validate_dashboard_host(cls, v: str) -> str:
        """Warn if the dashboard host is not localhost."""
        if v not in ("127.0.0.1", "::1", "localhost"):
            import warnings

            warnings.warn(
                f"Dashboard host '{v}' is not localhost. "
                "Exposing the dashboard externally is a security risk. "
                "Ensure you have appropriate network controls in place.",
                stacklevel=2,
            )
        return v


_settings: Settings | None = None


def get_settings() -> Settings:
    """Return the application settings singleton.

    Returns:
        The Settings instance, created on first call.
    """
    global _settings  # noqa: PLW0603
    if _settings is None:
        _settings = Settings()
    return _settings
