# PacketSnifferAnalyzer — Documentation

This directory contains the complete documentation for PacketSnifferAnalyzer.

## Structure

| Directory / File | Contents |
|---|---|
| `index.md` | Documentation home |
| `installation.md` | Per-platform installation guide |
| `quickstart.md` | Get capturing in 60 seconds |
| `cli-reference.md` | Complete CLI command reference |
| `architecture.md` | System architecture and design |
| `plugins.md` | Plugin development guide |
| `security.md` | Security model and threat analysis |
| `contributing.md` | Contribution guide (mirrors CONTRIBUTING.md) |
| `troubleshooting.md` | Common issues and solutions |
| `api/` | Web dashboard API reference |
| `adr/` | Architecture Decision Records |
| `runbooks/` | Operational runbooks |
| `monitoring/` | Monitoring and alerting guide |
| `deployment/` | Deployment guide |
| `operations/` | Operations guide |

## Building the Documentation

```bash
# Install documentation dependencies
pip install -e ".[dev]"

# Build
mkdocs build

# Serve locally
mkdocs serve
# Open http://127.0.0.1:8000
```
