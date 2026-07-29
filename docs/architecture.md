# System Architecture

PacketSnifferAnalyzer uses **Clean Architecture** with a **Hexagonal (Ports and Adapters)** pattern. This document describes the system design, component responsibilities, data flows, and concurrency model.

---

## Architecture Principles

1. **Dependency Rule:** Source code dependencies point inward only. The domain layer has zero dependencies on external libraries, UI frameworks, or infrastructure.
2. **Ports and Adapters:** All external concerns (capture backends, storage, UI) are adapters that implement abstract port interfaces.
3. **Testability:** Every component can be tested in isolation by substituting adapters with mocks.
4. **Extensibility:** New capture backends, storage formats, and UI modes can be added without modifying the domain or use case layers.

---

## Layer Diagram

```
┌───────────────────────────────────────────────────────────┐
│                    Interface Layer                        │
│         CLI Adapter │ GUI Adapter │ Web Adapter           │
├───────────────────────────────────────────────────────────┤
│                  Application Layer                        │
│    Use Cases: StartCapture, StopCapture, ExportSession     │
├───────────────────────────────────────────────────────────┤
│                    Domain Layer                           │
│   Packet, Flow, Protocol, AlertRule, Session, Filter      │
├───────────────────────────────────────────────────────────┤
│                Infrastructure Layer                       │
│  ScapyCapture │ PcapStorage │ Plugins │ Logging │ Config │
└───────────────────────────────────────────────────────────┘
```

---

## Component Responsibilities

| Component | Package | Responsibility |
|---|---|---|
| **Domain Models** | `domain/` | Pure data structures; no external deps |
| **Port Interfaces** | `ports/` | Abstract contracts for all adapters |
| **Use Cases** | `use_cases/` | Orchestrate domain + ports; business logic |
| **Capture Adapter** | `adapters/capture/` | Raw packet acquisition |
| **Dissection Adapter** | `adapters/dissection/` | Protocol layer decoding |
| **Storage Adapter** | `adapters/storage/` | PCAP read/write, session persistence |
| **Notification Adapter** | `adapters/notification/` | Alert output (console, webhook) |
| **CLI Adapter** | `interfaces/cli/` | Terminal interface (Click) |
| **GUI Adapter** | `interfaces/gui/` | Desktop interface (PyQt6) |
| **Web Adapter** | `interfaces/web/` | Browser interface (FastAPI + HTMX) |
| **Plugin Manager** | `plugins/` | Plugin discovery and lifecycle |
| **Infrastructure** | `infrastructure/` | Logging, config, audit, privilege, encryption |

---

## Data Flow

```
Network Interface
      │
      ▼
[Capture Engine] ──BPF filter──► [Packet Queue (ring buffer)]
      │
      ▼
[Dissection Engine] ──► [Domain Packet Model]
      │
      ├──► [Filter Engine] ──► [Display Queue]
      ├──► [Analysis Engine] ──► [Statistics Store]
      ├──► [Alert Engine] ──► [Alert Queue]
      ├──► [Plugin Manager] ──► [Plugin Callbacks]
      └──► [Storage Engine] ──► [PCAP / JSON / CSV]
                │
                ▼
    [CLI / GUI / Web Adapter] ◄── [Display Queue + Statistics Store]
```

---

## Concurrency Model

| Thread | Role | Priority |
|---|---|---|
| **Capture thread** | Reads from network interface; feeds ring buffer | High |
| **Dissection workers** | Thread pool consuming ring buffer; decode protocols | Normal |
| **Analysis thread** | Consumes dissected packets; updates statistics | Normal |
| **Alert thread** | Evaluates rules against analysis state | Normal |
| **UI thread** | Reads display queue at refresh rate; never blocks | Normal |
| **Storage thread** | Writes packets to PCAP; flushes periodically | Low |

**GIL mitigation:** Python's GIL limits true CPU parallelism. For high-throughput scenarios (> 100k pkt/s), dissection workers use `multiprocessing` with shared memory queues. For typical workloads, threading is sufficient.

---

## Security Architecture

See [security.md](security.md) for the full security model.

Key boundaries:
- Packet payloads never enter the logging subsystem
- Web dashboard binds to `127.0.0.1` by default
- Privilege drop occurs after interface binding on Linux
- Plugin errors are isolated; plugins cannot crash the core engine

---

## Technology Stack

| Layer | Technology | Justification |
|---|---|---|
| Language | Python 3.11+ | Networking ecosystem; accessibility |
| Capture | Scapy 2.5 | Industry standard; extensible |
| CLI | Click 8 | Ergonomic; composable commands |
| GUI | PyQt6 | Mature; cross-platform; LGPL |
| Web backend | FastAPI | Async; WebSocket; auto-docs |
| Web frontend | HTMX + Alpine.js | Minimal JS; server-driven |
| Charts | Chart.js | Lightweight; real-time capable |
| Logging | structlog | Structured JSON; context binding |
| Config | Pydantic Settings | Type-safe; env var support |
| Encryption | cryptography (AES-256-GCM) | Industry standard |
| KDF | argon2-cffi (Argon2id) | Modern; memory-hard |
| Testing | pytest | Industry standard |
| Linting | ruff | Fast; replaces flake8+black+isort |
| Type checking | mypy --strict | Catches type errors early |
