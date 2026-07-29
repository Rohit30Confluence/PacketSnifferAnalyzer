# Troubleshooting Guide

This guide covers common issues and their solutions.

---

## Privilege Errors

### `PermissionError: [Errno 1] Operation not permitted`

**Cause:** Raw packet capture requires elevated privileges.

**Solutions:**

```bash
# Linux / macOS: Run with sudo
sudo psa capture start --interface eth0

# Linux: Grant capabilities to Python
sudo setcap cap_net_raw,cap_net_admin+eip $(which python)

# Windows: Run terminal as Administrator
```

---

## Interface Errors

### `ValueError: Interface 'None' not found`

**Cause:** No network interfaces were detected. Common in sandboxed environments.

**Diagnosis:**
```bash
python -c "from scapy.all import get_if_list; print(get_if_list())"
```

**Solutions:**
- Ensure the system is not fully sandboxed (some CI environments block raw sockets)
- On Windows, verify Npcap is installed with WinPcap API-compatible mode
- On Linux, verify libpcap is installed: `sudo apt-get install libpcap-dev`

### `Interface 'eth0' not found`

**Cause:** The specified interface name does not exist.

**Solution:** Run `psa interfaces` to list available interfaces, then use the correct name.

---

## Filter Errors

### `FilterSyntaxError: Invalid BPF filter`

**Cause:** The BPF filter expression contains a syntax error.

**Solution:** Validate your filter with `tcpdump -d "your filter"` before using it with `psa`.

Common mistakes:
- `tcp port80` → `tcp port 80` (missing space)
- `ip.src == 1.2.3.4` → `src host 1.2.3.4` (BPF syntax, not display filter syntax)

---

## Installation Errors

### `ModuleNotFoundError: No module named 'scapy'`

**Solution:**
```bash
pip install packetsnifferanalyzer
# or
pip install scapy
```

### `ModuleNotFoundError: No module named 'PyQt6'`

**Solution:**
```bash
pip install "packetsnifferanalyzer[gui]"
# or
pip install PyQt6
```

### `ImportError: libpcap.so.0.8: cannot open shared object file`

**Solution (Linux):**
```bash
sudo apt-get install libpcap0.8
# or
sudo dnf install libpcap
```

---

## Windows-Specific Issues

### Npcap not detected

1. Download and install [Npcap](https://npcap.com/)
2. During installation, check **"WinPcap API-compatible mode"**
3. Restart your terminal
4. Run `psa interfaces` to verify

### `Access is denied` on Windows

Right-click your terminal and select **"Run as Administrator"**.

---

## Performance Issues

### High packet drop rate

**Symptoms:** `psa capture status` shows a high drop count.

**Solutions:**
- Increase the ring buffer size: `PSA_RING_BUFFER_SIZE=131072 psa capture start ...`
- Apply a more specific BPF filter to reduce capture volume
- Use a faster storage device for PCAP output
- Reduce the number of active plugins

### GUI becomes unresponsive during high-rate capture

**Solution:** Reduce the display refresh rate in Settings, or use the CLI for high-rate captures.

---

## Diagnostic Commands

```bash
# Check version
psa --version

# List interfaces
psa interfaces

# Check Scapy interface detection
python -c "from scapy.all import get_if_list; print(get_if_list())"

# Check privileges
python -c "import os; print('UID:', os.getuid() if hasattr(os, 'getuid') else 'N/A')"

# Run with debug logging
psa --debug capture start --interface eth0

# Check installed version
pip show packetsnifferanalyzer
```

---

## Getting Help

1. Check this troubleshooting guide
2. Search [existing issues](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/-/issues)
3. Open a [bug report](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/-/issues/new?issuable_template=bug_report) with full diagnostic output
