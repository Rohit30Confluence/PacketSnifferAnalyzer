"""Privilege detection and management.

This module handles the detection of required OS privileges for raw
packet capture and provides guidance when privileges are insufficient.

On Linux, the minimum required capabilities are:
  - CAP_NET_RAW: Required for raw socket access
  - CAP_NET_ADMIN: Required for interface configuration

On macOS and Windows, root/Administrator access is required.
"""

from __future__ import annotations

import os
import platform
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class PrivilegeStatus:
    """The result of a privilege check.

    Attributes:
        has_sufficient_privileges: True if capture can proceed.
        method: How privileges were determined.
        remediation: Instructions for obtaining required privileges.
    """

    has_sufficient_privileges: bool
    method: str
    remediation: str


def check_privileges() -> PrivilegeStatus:
    """Check whether the current process has sufficient privileges for capture.

    Returns:
        A PrivilegeStatus describing the current privilege state and
        remediation steps if privileges are insufficient.
    """
    system = platform.system()

    if system == "Linux":
        return _check_linux_privileges()
    elif system == "Darwin":
        return _check_macos_privileges()
    elif system == "Windows":
        return _check_windows_privileges()
    else:
        return PrivilegeStatus(
            has_sufficient_privileges=False,
            method="unknown_platform",
            remediation=(
                f"Unsupported platform: {system}. "
                "PacketSnifferAnalyzer supports Linux, macOS, and Windows."
            ),
        )


def _check_linux_privileges() -> PrivilegeStatus:
    """Check Linux-specific capture privileges."""
    if os.geteuid() == 0:
        return PrivilegeStatus(
            has_sufficient_privileges=True,
            method="root",
            remediation="",
        )

    # Check for CAP_NET_RAW capability
    try:
        import ctypes
        import ctypes.util

        libcap = ctypes.CDLL(ctypes.util.find_library("cap"))
        # Simplified check — full capability check implemented in Phase 1
        _ = libcap
        has_cap = False  # Placeholder until Phase 1 implementation
    except Exception:  # noqa: BLE001
        has_cap = False

    if has_cap:
        return PrivilegeStatus(
            has_sufficient_privileges=True,
            method="cap_net_raw",
            remediation="",
        )

    return PrivilegeStatus(
        has_sufficient_privileges=False,
        method="insufficient",
        remediation=(
            "Raw packet capture requires elevated privileges on Linux.\n"
            "Options:\n"
            "  1. Run with sudo: sudo psa capture start ...\n"
            "  2. Grant capabilities: sudo setcap cap_net_raw,cap_net_admin+eip "
            f"{sys.executable}\n"
            "  3. Use Docker with --cap-add NET_RAW NET_ADMIN"
        ),
    )


def _check_macos_privileges() -> PrivilegeStatus:
    """Check macOS-specific capture privileges."""
    if os.geteuid() == 0:
        return PrivilegeStatus(
            has_sufficient_privileges=True,
            method="root",
            remediation="",
        )

    return PrivilegeStatus(
        has_sufficient_privileges=False,
        method="insufficient",
        remediation=(
            "Raw packet capture requires root on macOS.\n"
            "Run with: sudo psa capture start ..."
        ),
    )


def _check_windows_privileges() -> PrivilegeStatus:
    """Check Windows-specific capture privileges."""
    try:
        import ctypes

        is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        is_admin = False

    if is_admin:
        return PrivilegeStatus(
            has_sufficient_privileges=True,
            method="administrator",
            remediation="",
        )

    return PrivilegeStatus(
        has_sufficient_privileges=False,
        method="insufficient",
        remediation=(
            "Raw packet capture requires Administrator privileges on Windows.\n"
            "Right-click your terminal and select 'Run as Administrator', "
            "then run psa again.\n"
            "Also ensure Npcap is installed: https://npcap.com/"
        ),
    )
