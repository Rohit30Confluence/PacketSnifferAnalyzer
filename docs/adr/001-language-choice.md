# ADR-001: Python as Primary Language

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Dr.Confluence-group

---

## Context

PacketSnifferAnalyzer needs a language that:
- Has a mature networking and packet manipulation ecosystem
- Is accessible to a wide range of contributors (students, researchers, engineers)
- Supports all three interface modes (CLI, GUI, web)
- Can be distributed easily across Linux, macOS, and Windows

## Decision

Python 3.10+ is the primary language.

## Rationale

- **Ecosystem:** Scapy, the de facto standard for Python packet manipulation, is Python-native. No other language has an equivalent library with the same breadth of protocol support.
- **Accessibility:** Python is the most widely taught language in networking and security curricula. This maximizes the contributor pool.
- **Cross-platform:** Python runs on all three target platforms with minimal platform-specific code.
- **Tooling:** The Python ecosystem has excellent tooling for testing (pytest), type checking (mypy), linting (ruff), and packaging (pyproject.toml).

## Alternatives Considered

| Language | Reason Rejected |
|---|---|
| Go | No equivalent to Scapy; GUI ecosystem is immature |
| Rust | Steep learning curve; smaller contributor pool; no Scapy equivalent |
| C++ | High complexity; memory safety concerns; poor packaging story |
| Java | Verbose; no Scapy equivalent; GUI (Swing/JavaFX) is dated |

## Consequences

- **Positive:** Large contributor pool; rich ecosystem; rapid development
- **Negative:** GIL limits CPU parallelism; slower than compiled languages at high packet rates
- **Mitigation:** Use `multiprocessing` for CPU-bound dissection at high throughput; use C extensions via Scapy's libpcap bindings for the hot path
