# PacketSnifferAnalyzer

A Python-based network packet analysis platform for **live traffic capture, protocol dissection, packet inspection, flow analysis, security detection, and traffic visualization**.

Built around a **Clean Architecture + Hexagonal Ports & Adapters** design so capture engines, protocol dissectors, detection logic, storage, and user interfaces remain independently testable.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/Tests-53%20passing-brightgreen)
![Architecture](https://img.shields.io/badge/Architecture-Clean%20%2B%20Hexagonal-purple)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)
![License](https://img.shields.io/badge/License-Unlicense-green)

---

## Overview

PacketSnifferAnalyzer is being developed as a practical **network-security analysis platform**, rather than a basic packet-printing script.

The project is designed to process both live traffic and recorded captures through a layered analysis pipeline:

```text
Network / PCAP
      │
      ▼
Capture Adapter
      │
      ▼
Raw Packet
      │
      ▼
Protocol Dissection
      │
      ▼
Normalized Domain Packet
      │
      ▼
Flow / Feature Analysis
      │
      ▼
Security Detection
      │
      ├── CLI
      ├── GUI
      ├── Web Dashboard
      └── Evidence / Export
```

The architecture separates packet acquisition from analysis so the same core can eventually process live interfaces, PCAP files, test fixtures, and recorded sessions.

---

## Current Status

### Implemented

The current milestone establishes the core packet-dissection foundation.

- Clean Architecture / Ports & Adapters foundation
- Scapy-based packet dissection pipeline
- Ethernet dissection
- IPv4 dissection
- TCP dissection
- UDP dissection
- Normalized domain packet representation
- Layer-level raw byte preservation
- Packet parse-error handling
- Protocol dispatch through `ScapyDissector`
- Unit tests for protocol dissectors
- Orchestrator-level dissection tests
- Automated test suite

### Current Verification

```text
53 tests passing
```

The repository is actively being developed toward a complete network-security analysis workflow.

---

## Supported Protocol Dissection

| Protocol | Status |
|---|---|
| Ethernet | Implemented |
| IPv4 | Implemented |
| TCP | Implemented |
| UDP | Implemented |
| DNS | Planned |
| ARP | Planned |
| TLS metadata | Planned |
| HTTP metadata | Planned |
| ICMP | Planned |
| IPv6 | Planned |

The protocol layer is intentionally modular so additional dissectors can be introduced without coupling the domain model directly to Scapy-specific implementation details.

---

## Security Detection Roadmap

The analysis engine is intended to support practical defensive network-security detections such as:

- TCP SYN scanning
- UDP scanning
- SYN flood indicators
- ARP spoofing indicators
- DNS anomalies
- Repeated connection attempts
- Beaconing patterns
- Suspicious port activity
- Abnormal traffic-volume patterns
- MITRE ATT&CK technique mapping

Detection logic will operate on normalized packets and flow-level features rather than being tightly coupled to the packet-capture implementation.

---

## Architecture

PacketSnifferAnalyzer follows **Clean Architecture** and **Hexagonal Architecture (Ports & Adapters)** principles.

High-level structure:

```text
src/packetanalyzer/

domain/
    packet models
    sessions
    analysis entities

ports/
    capture
    dissection
    analysis
    storage

adapters/
    capture
    dissection
    storage
    presentation

application/
    use cases
    orchestration

infrastructure/
    configuration
    logging
```

The core domain is designed to remain independent from network-capture libraries and presentation frameworks wherever practical.

Detailed architecture documentation:

```text
docs/architecture.md
```

---

## Analysis Pipeline

The long-term processing pipeline is:

```text
Capture
   ↓
Normalize
   ↓
Dissect
   ↓
Flow Correlation
   ↓
Feature Extraction
   ↓
Detection Engine
   ↓
Evidence Store
   ↓
Visualization / Export
```

This separation allows the same analysis engine to work with:

- Live network traffic
- PCAP files
- PCAPNG files
- Recorded sessions
- Automated test fixtures

---

## Project Structure

```text
PacketSnifferAnalyzer/
├── docker/
├── docs/
├── examples/
├── plugins/
├── requirements/
├── scripts/
├── src/
│   └── packetanalyzer/
├── tests/
├── docker-compose.yml
├── mkdocs.yml
├── pyproject.toml
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Rohit30Confluence/PacketSnifferAnalyzer.git
cd PacketSnifferAnalyzer
```

The project requires **Python 3.10 or newer**.

### Create a virtual environment

Example using Python 3.12:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### Install the project

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

---

## Testing

Run the complete test suite:

```bash
pytest
```

Current milestone:

```text
53 passed
```

Run with coverage:

```bash
pytest --cov=packetanalyzer
```

Run static checks:

```bash
ruff check .
```

Check Git whitespace errors:

```bash
git diff --check
```

---

## CLI

The project exposes the `psa` command.

Display available commands:

```bash
psa --help
```

Planned/active command areas include:

```bash
psa interfaces
psa capture
psa analyze
psa export
psa dashboard
psa gui
```

Live-capture functionality is being implemented incrementally, so command interfaces may evolve during development.

---

## Live Capture

The next major implementation milestone is the capture adapter.

Planned capabilities include:

- Network-interface discovery
- Live packet capture
- Capture start/stop lifecycle
- Pause/resume support
- Packet callbacks
- BPF filtering
- Capture statistics
- Drop-count reporting
- Controlled shutdown
- Testable capture abstraction

The capture layer will feed the existing dissection pipeline rather than duplicating protocol-processing logic.

---

## PCAP / PCAPNG Analysis

Recorded traffic support is planned as a first-class input path.

The intended workflow is:

```text
PCAP / PCAPNG
      ↓
Capture Adapter
      ↓
Raw Packet
      ↓
ScapyDissector
      ↓
Normalized Packet
      ↓
Analysis
```

This allows offline investigation without requiring privileged live packet capture.

---

## Testing Philosophy

The project prioritizes **real functionality backed by automated verification**.

Protocol dissectors are tested independently using generated packet structures.

The dissection orchestrator is tested separately to verify:

- Protocol identification
- Layer dispatch
- Normalized layer creation
- Raw-byte preservation
- Parse-error handling
- Multi-layer packet processing

The architecture is designed so future capture and detection components can also be tested without requiring privileged access to a real network interface.

---

## Development Roadmap

| Milestone | Focus | Status |
|---|---|---|
| M1 | Domain + protocol dissection foundation | **Complete** |
| M2 | Live capture + interface management + BPF | **Next** |
| M3 | PCAP / PCAPNG ingestion | Planned |
| M4 | Flow / connection tracking | Planned |
| M5 | Traffic feature extraction | Planned |
| M6 | Network-security detection engine | Planned |
| M7 | Evidence / forensic workflows | Planned |
| M8 | Dashboard + API | Planned |
| M9 | Performance benchmarking and hardening | Planned |

---

## Security Use Cases

The project is intended to support authorized defensive and research workflows including:

### Network Monitoring

Inspect:

- Source and destination addresses
- Source and destination ports
- Protocol distribution
- Packet sizes
- Traffic volume
- Network conversations

### Security Analysis

Identify patterns associated with:

- Scanning
- Flooding
- Suspicious repeated connections
- DNS anomalies
- ARP manipulation
- Beacon-like communication
- Abnormal traffic behavior

### Forensics

Future evidence workflows will support:

- Capture preservation
- Packet/session correlation
- Structured event records
- Detection evidence
- Machine-readable exports

---

## Responsible Use

Packet capture can expose sensitive network information.

Only capture traffic on networks, systems, and interfaces that you own or are explicitly authorized to monitor.

This project is intended for:

- Security research
- Network troubleshooting
- Defensive monitoring
- Authorized penetration testing
- Cybersecurity education
- Digital forensics experimentation

Do not use PacketSnifferAnalyzer to intercept traffic without authorization.

---

## Documentation

| Document | Purpose |
|---|---|
| `docs/architecture.md` | Architecture and component design |
| `docs/installation.md` | Installation guidance |
| `docs/quickstart.md` | Quick-start workflow |
| `docs/cli-reference.md` | CLI reference |
| `docs/plugins.md` | Plugin development |
| `docs/security.md` | Security considerations |

---

## Contributing

Contributions and technical feedback are welcome.

Before making substantial changes:

1. Review the architecture.
2. Review existing tests.
3. Keep domain logic independent from infrastructure.
4. Add automated tests for new functionality.
5. Run the test suite before submitting changes.

---

## License

Released under the [Unlicense](LICENSE) and dedicated to the public domain.