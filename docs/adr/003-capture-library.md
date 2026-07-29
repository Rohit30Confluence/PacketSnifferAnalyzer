# ADR-003: Scapy as Capture and Dissection Backend

**Status:** Accepted
**Date:** 2026-07-29
**Deciders:** Dr.Confluence-group

---

## Context

The system needs a library for raw packet capture and protocol dissection that:
- Supports a wide range of protocols out of the box
- Is extensible for custom protocols
- Works on Linux, macOS, and Windows
- Is actively maintained

## Decision

Use Scapy 2.5 as the primary capture and dissection backend, abstracted behind the `CapturePort` and `DissectorPort` interfaces.

## Rationale

- **Protocol breadth:** Scapy supports hundreds of protocols natively, more than any other Python library.
- **Extensibility:** Custom protocols can be defined as Scapy packet classes.
- **Cross-platform:** Scapy works on Linux (via libpcap), macOS (via libpcap), and Windows (via Npcap).
- **Community:** Scapy has a large, active community and is widely used in security research.
- **Abstraction:** By placing Scapy behind a port interface, it can be replaced with a different backend (e.g., dpkt, pyshark, or a C extension) without changing the domain layer.

## Alternatives Considered

| Library | Reason Rejected |
|---|---|
| dpkt | Lower-level; less protocol support; less active |
| pyshark | Wraps tshark; adds external dependency; slower |
| libpcap (ctypes) | Too low-level; requires manual protocol parsing |
| Raw sockets | Platform-specific; no protocol dissection |

## Consequences

- **Positive:** Rich protocol support; extensible; well-documented
- **Negative:** Scapy's sniff() is blocking; requires threading; Windows requires Npcap
- **Mitigation:** Capture runs in a dedicated thread; Npcap installation is documented
