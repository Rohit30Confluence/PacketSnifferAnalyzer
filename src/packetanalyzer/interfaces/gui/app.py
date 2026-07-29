"""PyQt6 desktop GUI application entry point.

The GUI adapter provides a full-featured desktop interface with:
  - Packet list view with virtual scrolling
  - Protocol detail tree
  - Hex dump panel
  - Filter bar with real-time validation
  - Capture controls (Start/Stop/Pause/Resume)
  - Statistics panel with live charts
  - Dark and light theme support

This module is a scaffold. The full implementation will be added
in Milestone 4 (Epic 5).
"""

from __future__ import annotations

import sys


def run_gui() -> int:
    """Launch the PyQt6 desktop GUI.

    Returns:
        The application exit code.

    Raises:
        ImportError: If PyQt6 is not installed. Install with:
            pip install packetsnifferanalyzer[gui]
    """
    try:
        from PyQt6.QtWidgets import QApplication  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "PyQt6 is required for the GUI interface. "
            "Install it with: pip install packetsnifferanalyzer[gui]"
        ) from exc

    app = QApplication(sys.argv)
    app.setApplicationName("PacketSnifferAnalyzer")
    app.setApplicationVersion("0.1.0-alpha.1")
    app.setOrganizationName("Dr.Confluence-group")

    # Full GUI implementation in Phase 3 — M4
    # from packetanalyzer.interfaces.gui.main_window import MainWindow
    # window = MainWindow()
    # window.show()
    # return app.exec()

    print("GUI will be available in Phase 3 (M4).")
    return 0
