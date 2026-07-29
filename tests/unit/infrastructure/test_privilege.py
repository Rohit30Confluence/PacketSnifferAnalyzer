"""Unit tests for the privilege detection module."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from packetanalyzer.infrastructure.privilege import PrivilegeStatus, check_privileges


@pytest.mark.unit
class TestPrivilegeStatus:
    """Tests for the PrivilegeStatus dataclass."""

    def test_privilege_status_creation(self) -> None:
        """PrivilegeStatus can be created with required fields."""
        status = PrivilegeStatus(
            has_sufficient_privileges=True,
            method="root",
            remediation="",
        )
        assert status.has_sufficient_privileges is True
        assert status.method == "root"

    def test_privilege_status_is_frozen(self) -> None:
        """PrivilegeStatus is immutable."""
        status = PrivilegeStatus(
            has_sufficient_privileges=False,
            method="insufficient",
            remediation="Run with sudo.",
        )
        with pytest.raises(AttributeError):
            status.has_sufficient_privileges = True  # type: ignore[misc]


@pytest.mark.unit
class TestCheckPrivileges:
    """Tests for the check_privileges function."""

    def test_returns_privilege_status(self) -> None:
        """check_privileges always returns a PrivilegeStatus."""
        status = check_privileges()
        assert isinstance(status, PrivilegeStatus)

    @patch("packetanalyzer.infrastructure.privilege.platform.system", return_value="Linux")
    @patch("packetanalyzer.infrastructure.privilege.os.geteuid", return_value=0)
    def test_linux_root_has_privileges(self, mock_geteuid: object, mock_system: object) -> None:
        """On Linux, root (uid 0) has sufficient privileges."""
        status = check_privileges()
        assert status.has_sufficient_privileges is True
        assert status.method == "root"

    @patch("packetanalyzer.infrastructure.privilege.platform.system", return_value="Linux")
    @patch("packetanalyzer.infrastructure.privilege.os.geteuid", return_value=1000)
    def test_linux_non_root_lacks_privileges(self, mock_geteuid: object, mock_system: object) -> None:
        """On Linux, non-root without capabilities lacks privileges."""
        status = check_privileges()
        assert status.has_sufficient_privileges is False
        assert "sudo" in status.remediation.lower() or "cap" in status.remediation.lower()

    @patch("packetanalyzer.infrastructure.privilege.platform.system", return_value="Darwin")
    @patch("packetanalyzer.infrastructure.privilege.os.geteuid", return_value=0)
    def test_macos_root_has_privileges(self, mock_geteuid: object, mock_system: object) -> None:
        """On macOS, root has sufficient privileges."""
        status = check_privileges()
        assert status.has_sufficient_privileges is True

    @patch("packetanalyzer.infrastructure.privilege.platform.system", return_value="Unknown")
    def test_unknown_platform_lacks_privileges(self, mock_system: object) -> None:
        """On an unknown platform, privileges are reported as insufficient."""
        status = check_privileges()
        assert status.has_sufficient_privileges is False
