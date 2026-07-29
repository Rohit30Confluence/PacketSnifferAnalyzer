# ADR-004: PyQt6 for Desktop GUI

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Dr.Confluence-group

---

## Context

The desktop GUI needs to:
- Display tens of thousands of packets with virtual scrolling
- Render a protocol detail tree and hex dump panel
- Update in real time during capture
- Run on Linux, macOS, and Windows
- Be compatible with the Unlicense (public domain) project license

## Decision

Use PyQt6 for the desktop GUI.

## Rationale

- **Maturity:** Qt is a 30-year-old, battle-tested GUI framework used in production applications including Wireshark.
- **Performance:** Qt's model/view architecture with virtual scrolling handles millions of rows efficiently.
- **Cross-platform:** PyQt6 produces native-looking UIs on all three target platforms.
- **License:** PyQt6 is licensed under GPL v3 and LGPL v3. For a public domain project, LGPL is compatible when PyQt6 is used as a dynamically linked library (the default).
- **Ecosystem:** PyQtGraph provides high-performance real-time charts built on Qt.

## Alternatives Considered

| Framework | Reason Rejected |
|---|---|
| Tkinter | Too limited for a professional packet analysis UI; no virtual scrolling; dated appearance |
| wxPython | Less active; smaller community; fewer widgets |
| Dear PyGui | Excellent performance but immature; limited widget set |
| Electron | 200 MB+ runtime; overkill for a local tool |
| PySide6 | Functionally equivalent to PyQt6; LGPL only; considered as fallback |

## Consequences

- **Positive:** Professional-grade UI; high performance; cross-platform
- **Negative:** Large dependency; requires separate `[gui]` install extra
- **Mitigation:** GUI is optional; CLI and web dashboard work without PyQt6
