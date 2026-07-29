# Installation Guide

This guide covers installation of PacketSnifferAnalyzer on Linux, macOS, and Windows.

---

## Prerequisites

### All Platforms

- Python 3.10, 3.11, or 3.12
- pip 23.0 or later
- Git (for source installation)

### Linux

Install libpcap development headers:

```bash
# Debian / Ubuntu / Mint
sudo apt-get update
sudo apt-get install -y libpcap-dev python3-dev

# Fedora / RHEL / CentOS
sudo dnf install -y libpcap-devel python3-devel

# Arch Linux
sudo pacman -S libpcap
```

### macOS

libpcap is included with Xcode Command Line Tools:

```bash
xcode-select --install
```

If you use Homebrew:
```bash
brew install libpcap
```

### Windows

1. Install [Npcap](https://npcap.com/) — the modern replacement for WinPcap.
   - During installation, check **"WinPcap API-compatible mode"**.
2. Install [Python 3.11](https://www.python.org/downloads/windows/) (64-bit recommended).
3. Ensure Python is added to your PATH.

---

## Installation Methods

### Method 1: PyPI (Recommended)

```bash
pip install packetsnifferanalyzer
```

With GUI support:
```bash
pip install "packetsnifferanalyzer[gui]"
```

### Method 2: From Source

```bash
# Clone the repository
git clone https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer.git
cd PacketSnifferAnalyzer

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Linux / macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Install in editable mode with all dependencies
pip install -e ".[dev,gui]"

# Install pre-commit hooks (for contributors)
pre-commit install
```

### Method 3: Docker

```bash
# Clone the repository
git clone https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer.git
cd PacketSnifferAnalyzer

# Start the development environment
docker compose up -d

# Access the container
docker compose exec app bash

# Run commands
docker compose exec app psa interfaces
```

---

## Privilege Configuration

Raw packet capture requires elevated privileges. Choose the method appropriate for your environment.

### Linux: sudo (Simplest)

```bash
sudo psa capture start --interface eth0
```

### Linux: Capabilities (Recommended for Regular Use)

Grant the Python interpreter the minimum required capabilities:

```bash
# Find your Python executable
which python
# Example: /home/user/.venv/bin/python

# Grant capabilities
sudo setcap cap_net_raw,cap_net_admin+eip /home/user/.venv/bin/python

# Verify
cap_net_raw /home/user/.venv/bin/python

# Now run without sudo
psa capture start --interface eth0
```

**Note:** Re-run `setcap` after upgrading Python or recreating the virtual environment.

### Linux: Docker with NET_RAW

The provided `docker-compose.yml` grants `NET_RAW` and `NET_ADMIN` capabilities automatically.

### macOS

```bash
sudo psa capture start --interface en0
```

### Windows

Right-click your terminal (Command Prompt or PowerShell) and select **"Run as Administrator"**, then run `psa`.

---

## Verifying the Installation

```bash
# Check the version
psa --version

# List available interfaces (requires privileges)
psa interfaces

# Run the test suite (no privileges required)
pytest tests/unit/
```

---

## Upgrading

```bash
# PyPI installation
pip install --upgrade packetsnifferanalyzer

# Source installation
git pull origin main
pip install -e ".[dev,gui]"
```

---

## Uninstalling

```bash
pip uninstall packetsnifferanalyzer

# Remove session data and logs (optional)
rm -rf ~/.packetanalyzer
```

---

## Troubleshooting

See [troubleshooting.md](troubleshooting.md) for common installation issues.
