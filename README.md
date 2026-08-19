# PacketSnifferAnalyzer

A Python-based packet sniffer and traffic analyzer with a CLI, a GUI, and a dashboard visualizer.

One capture engine, three ways to look at the same traffic — the terminal user, the point-and-click user, and the person who just wants a dashboard to glance at.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Unlicense-green)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

---

## Overview

PacketSnifferAnalyzer captures live network traffic and gives you three interfaces to work with it:

- **CLI** — filterable live capture output, scriptable and pipeable
- **GUI** — a desktop window for browsing and inspecting packets
- **Dashboard** — aggregate traffic visualization: protocol mix, top talkers, volume over time

All three sit on top of one shared capture core, so they stay in sync without duplicating logic.

---

## Architecture

```
Interface → Capture Engine → Parser → Analyzer → CLI / GUI / Dashboard
```

- **Capture Engine** — pulls raw packets off a network interface
- **Parser** — decodes protocol layers (Ethernet, IP, TCP/UDP)
- **Analyzer** — aggregates parsed packets into stats and patterns
- **Interfaces** — CLI, GUI, and Dashboard each consume the same analyzed data

---

## Features

- Live packet sniffing from a chosen network interface
- Protocol-level breakdown (Ethernet / IP / TCP / UDP)
- Packet-level inspection — drill from summary to individual packet
- Dashboard view of traffic volume, protocol mix, and top talkers
- Save and load capture sessions

---

## Installation

```bash
git clone https://github.com/Rohit30Confluence/PacketSnifferAnalyzer.git
cd PacketSnifferAnalyzer
```

Setup and dependency instructions will land here once the capture core ships (see [Roadmap](#roadmap)).

---

## Usage

```bash
# Planned CLI usage — subject to change
python -m packetsniffer capture --interface eth0
python -m packetsniffer capture --interface eth0 --filter tcp
python -m packetsniffer dashboard
```

---

## Roadmap

| Version | Milestone |
|---|---|
| v0.1 | Capture core — interface selection, raw packet capture, basic protocol parsing (Ethernet/IP/TCP/UDP) |
| v0.2 | CLI — filterable live capture output, save/load capture files |
| v0.3 | GUI — desktop packet list and inspector view |
| v0.4 | Dashboard — aggregate traffic visualization (volume, protocol mix, top talkers) |

---

## Contributing

The project is early and the architecture above is the current plan — issues and pull requests that help shape it are welcome. Open an issue before starting significant work so effort doesn't get duplicated.

---

## Security

This tool captures live network traffic. Only run it on networks and interfaces you own or are authorized to monitor. Unauthorized packet capture may be illegal in your jurisdiction.

---

## License

Released under the [Unlicense](LICENSE) — public domain.
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


