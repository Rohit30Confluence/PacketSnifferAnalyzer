# CLI Reference

Complete reference for all `psa` command-line interface commands.

---

## Global Options

```
psa [OPTIONS] COMMAND [ARGS]...
```

| Option | Description |
|---|---|
| `--version` | Show the version and exit |
| `--debug` | Enable debug logging to stderr |
| `--help` | Show help and exit |

---

## psa interfaces

List all available network interfaces on the host.

```bash
psa interfaces [OPTIONS]
```

| Option | Description |
|---|---|
| `--json` | Output as JSON |

**Examples:**
```bash
psa interfaces
psa interfaces --json
```

**Output columns:** NAME, STATUS (UP/DOWN), LOOPBACK, ADDRESSES

---

## psa capture

Manage packet capture sessions.

### psa capture start

```bash
sudo psa capture start [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--interface`, `-i` | Required | Network interface to capture on |
| `--filter`, `-f` | (none) | BPF filter expression |
| `--output`, `-o` | Auto-generated | Output PCAP file path |
| `--name`, `-n` | Auto-generated | Session name |
| `--encrypt` | False | Encrypt output with AES-256-GCM |
| `--count`, `-c` | 0 (unlimited) | Stop after N packets |

**Examples:**
```bash
sudo psa capture start -i eth0
sudo psa capture start -i wlan0 -f "tcp port 80"
sudo psa capture start -i eth0 -f "host 10.0.0.1" -o investigation.pcap
sudo psa capture start -i eth0 --encrypt --name "encrypted-session"
```

### psa capture stop

```bash
psa capture stop
```

Stops the active capture session and flushes all buffered packets to disk.

### psa capture pause

```bash
psa capture pause
```

Pauses the active capture. Packets arriving during a pause are discarded.

### psa capture resume

```bash
psa capture resume
```

Resumes a paused capture session.

### psa capture status

```bash
psa capture status [OPTIONS]
```

| Option | Description |
|---|---|
| `--json` | Output as JSON |

---

## psa analyze

Analyze an existing PCAP file.

```bash
psa analyze [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--file`, `-f` | Required | Path to the PCAP file |
| `--filter` | (none) | Display filter expression |
| `--stats` | False | Show traffic statistics |
| `--flows` | False | Show flow table |

**Examples:**
```bash
psa analyze --file capture.pcap
psa analyze -f capture.pcap --filter "ip.src == 192.168.1.1"
psa analyze -f capture.pcap --stats --flows
```

---

## psa export

Export a capture session to a file.

```bash
psa export [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--session`, `-s` | Required | Session ID or name |
| `--format`, `-f` | `pcap` | Export format: pcap, json, csv, text |
| `--output`, `-o` | Required | Output file path |
| `--filter` | (none) | Export only matching packets |
| `--redact-payload` | False | Replace payload bytes with zeros |

**Examples:**
```bash
psa export -s my-session -f json -o results.json
psa export -s my-session -f csv -o traffic.csv --redact-payload
psa export -s my-session -f pcap -o filtered.pcap --filter "tcp"
```

---

## psa dashboard

Manage the web dashboard server.

### psa dashboard start

```bash
psa dashboard start [OPTIONS]
```

| Option | Default | Description |
|---|---|---|
| `--host` | `127.0.0.1` | Host to bind to |
| `--port`, `-p` | `8080` | Port number |
| `--no-browser` | False | Do not open browser automatically |

**Security warning:** Changing `--host` from `127.0.0.1` exposes the dashboard to the network.

### psa dashboard stop

```bash
psa dashboard stop
```

---

## psa gui

Launch the desktop GUI.

```bash
psa gui
```

Requires PyQt6: `pip install packetsnifferanalyzer[gui]`

---

## BPF Filter Syntax

PacketSnifferAnalyzer uses standard Berkeley Packet Filter (BPF) syntax for pre-capture filters.

| Example | Description |
|---|---|
| `tcp` | All TCP traffic |
| `udp` | All UDP traffic |
| `port 80` | Traffic on port 80 (any protocol) |
| `tcp port 443` | TCP traffic on port 443 |
| `host 192.168.1.1` | Traffic to or from this host |
| `src host 10.0.0.1` | Traffic from this source |
| `dst port 53` | Traffic to port 53 (DNS) |
| `not arp` | Exclude ARP traffic |
| `tcp and port 80 or port 443` | HTTP or HTTPS |
| `net 192.168.0.0/24` | Traffic within this subnet |

For the complete BPF syntax reference, see `man pcap-filter`.

---

## Display Filter Syntax

Display filters are applied after capture and support field-level comparisons.

| Example | Description |
|---|---|
| `ip.src == 192.168.1.1` | Source IP equals |
| `tcp.dport == 443` | Destination port equals |
| `ip.ttl < 64` | TTL less than 64 |
| `tcp.flags.syn == 1` | SYN flag set |
| `dns.qname contains "example.com"` | DNS query contains string |
| `ip.src == 10.0.0.1 and tcp.dport == 80` | Compound filter |
| `not arp` | Exclude protocol |

---

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Insufficient privileges |
| 4 | Interface not found |
| 5 | Invalid filter syntax |
| 6 | Session not found |
