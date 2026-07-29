# PacketSnifferAnalyzer

[![Pipeline Status](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/badges/main/pipeline.svg)](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/-/pipelines)
[![Coverage](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/badges/main/coverage.svg)](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/-/commits/main)
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](https://unlicense.org)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A Python-based packet sniffer and network traffic analyzer with a CLI, desktop GUI, and real-time web dashboard. Built for network engineers, security researchers, and developers who need a transparent, auditable, and extensible alternative to heavyweight tools.

---

## ⚠️ Legal Notice

**Read this before using PacketSnifferAnalyzer.**

Packet capture on a network you do not own or have **explicit written authorization** to monitor may violate applicable laws, including but not limited to:

- Computer Fraud and Abuse Act (CFAA) — United States
- Computer Misuse Act — United Kingdom
- General Data Protection Regulation (GDPR) — European Union
- Equivalent legislation in your jurisdiction

Captured packets may contain personal data. You are solely responsible for compliance with applicable data protection and privacy laws. **The authors accept no liability for unauthorized use.**

By using this tool, you confirm that you have the legal right to capture traffic on the target network.

---

## Features

- **Live packet capture** from one or more network interfaces with BPF pre-filtering
- **Protocol dissection** for Ethernet, ARP, IPv4, IPv6, TCP, UDP, ICMP, DNS, DHCP, VLAN, TLS (metadata only)
- **Display filtering** with a composable filter DSL (AND / OR / NOT)
- **Real-time statistics**: packets/sec, bytes/sec, top talkers, protocol distribution, flow table
- **Session management**: named sessions, PCAP save/load, file rotation
- **Export**: PCAP, JSON, CSV, plain-text summary; optional payload redaction
- **Alert engine**: threshold-based rules with console, log, and webhook output
- **Plugin system**: load custom dissectors without modifying core code
- **Three interfaces**: CLI, PyQt6 desktop GUI, FastAPI + HTMX web dashboard
- **Offline analysis**: open any PCAP file without a live interface
- **Encrypted storage**: AES-256-GCM with Argon2id key derivation
- **Audit logging**: tamper-evident append-only session audit trail

---

## Requirements

| Requirement | Version |
|---|---|
| Python | 3.10, 3.11, or 3.12 |
| Operating System | Linux (primary), macOS (secondary), Windows (tertiary) |
| libpcap / Npcap | See platform notes below |

### Platform Notes

**Linux:** Install libpcap development headers.
```bash
# Debian / Ubuntu
sudo apt-get install libpcap-dev

# Fedora / RHEL
sudo dnf install libpcap-devel
```

**macOS:** libpcap is included with Xcode Command Line Tools.
```bash
xcode-select --install
```

**Windows:** Install [Npcap](https://npcap.com/) with the “WinPcap API-compatible mode” option enabled.

---

## Installation

### From PyPI (recommended)
```bash
pip install packetsnifferanalyzer
```

### From Source
```bash
git clone https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer.git
cd PacketSnifferAnalyzer
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### With Docker
```bash
docker compose up -d
docker compose exec app psa interfaces
```

---

## Quick Start

### CLI
```bash
# List available network interfaces
psa interfaces

# Start a live capture on eth0 with a BPF filter
sudo psa capture start --interface eth0 --filter "tcp port 80"

# Stop the capture
psa capture stop

# Open an existing PCAP file
psa analyze --file capture.pcap

# Export to JSON
psa export --session my-session --format json --output results.json

# Launch the web dashboard
psa dashboard start
```

### GUI
```bash
psa gui
```

### Web Dashboard
```bash
psa dashboard start --port 8080
# Opens http://127.0.0.1:8080 in your default browser
```

---

## Privileges

Raw packet capture requires elevated privileges on all platforms.

| Platform | Method |
|---|---|
| Linux | `sudo psa ...` or grant `CAP_NET_RAW` + `CAP_NET_ADMIN` |
| macOS | `sudo psa ...` |
| Windows | Run from an Administrator terminal |

The tool drops to minimum required privileges after interface binding on Linux.

---

## Architecture

PacketSnifferAnalyzer uses **Clean Architecture** with a **Hexagonal (Ports and Adapters)** pattern. The core domain has zero dependencies on UI frameworks, network libraries, or storage backends.

See [docs/architecture.md](docs/architecture.md) for the full architecture documentation.

---

## Documentation

| Document | Description |
|---|---|
| [Installation Guide](docs/installation.md) | Detailed per-platform installation |
| [Quick Start](docs/quickstart.md) | Get capturing in 60 seconds |
| [CLI Reference](docs/cli-reference.md) | All commands and options |
| [Architecture](docs/architecture.md) | System design and component map |
| [Plugin Development](docs/plugins.md) | Write custom dissectors |
| [Security](docs/security.md) | Security model and threat analysis |
| [Contributing](CONTRIBUTING.md) | How to contribute |
| [Changelog](CHANGELOG.md) | Release history |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a merge request. All contributors must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Security

To report a security vulnerability, please follow the process in [SECURITY.md](SECURITY.md). **Do not open a public issue for security vulnerabilities.**

---

## License

This project is released into the public domain under the [Unlicense](LICENSE). See [SECURITY.md](SECURITY.md) for responsible use requirements.
