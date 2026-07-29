# Quick Start Guide

Get from installation to your first packet capture in under 60 seconds.

---

## Before You Start

**Legal reminder:** Only capture traffic on networks you own or have explicit written authorization to monitor. See the [legal notice](../README.md#legal-notice) for details.

---

## Step 1: List Available Interfaces

```bash
# Linux / macOS (requires sudo)
sudo psa interfaces

# Example output:
# NAME       STATUS  ADDRESSES
# eth0       UP      192.168.1.100
# wlan0      UP      192.168.1.101
# lo         UP      127.0.0.1
# docker0    UP      172.17.0.1
```

---

## Step 2: Start a Capture

```bash
# Capture all traffic on eth0
sudo psa capture start --interface eth0

# Capture only TCP traffic on port 443 (HTTPS)
sudo psa capture start --interface eth0 --filter "tcp port 443"

# Capture and save to a named file
sudo psa capture start --interface eth0 --output my-capture.pcap

# Capture with a session name
sudo psa capture start --interface eth0 --name "morning-investigation"
```

---

## Step 3: View Live Statistics

While a capture is running, open a second terminal:

```bash
# View current session status
psa capture status

# View top talkers
psa top-talkers --n 10

# View active flows
psa flows
```

---

## Step 4: Stop the Capture

```bash
psa capture stop
```

---

## Step 5: Analyze and Export

```bash
# Analyze a saved PCAP file
psa analyze --file my-capture.pcap --stats

# Export to JSON
psa export --session morning-investigation --format json --output results.json

# Export to CSV with payload redaction
psa export --session morning-investigation --format csv --output traffic.csv --redact-payload
```

---

## Using the Web Dashboard

```bash
# Start the dashboard (opens browser automatically)
psa dashboard start

# Start on a custom port
psa dashboard start --port 9090

# Start without opening the browser
psa dashboard start --no-browser
```

The dashboard is available at `http://127.0.0.1:8080` by default.

---

## Using the Desktop GUI

```bash
# Requires: pip install packetsnifferanalyzer[gui]
psa gui
```

---

## Analyzing an Existing PCAP File

No live interface or elevated privileges required:

```bash
# Open a PCAP file
psa analyze --file capture.pcap

# Apply a display filter
psa analyze --file capture.pcap --filter "ip.src == 192.168.1.1"

# Show statistics
psa analyze --file capture.pcap --stats --flows
```

---

## Next Steps

- [CLI Reference](cli-reference.md) — All commands and options
- [Architecture](architecture.md) — How the system works
- [Plugin Development](plugins.md) — Write custom dissectors
- [Security](security.md) — Security model and best practices
