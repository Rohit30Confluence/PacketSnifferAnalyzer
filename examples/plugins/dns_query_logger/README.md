# DNS Query Logger Plugin

An example PacketSnifferAnalyzer plugin that logs DNS query names from captured traffic.

## What It Does

- Logs DNS query names (e.g., `example.com`) from DNS packets
- Counts total queries logged during the session
- Logs only queries (QR=0), not responses

## What It Does NOT Do

- Does not log DNS responses
- Does not log resolved IP addresses
- Does not log any packet payload data
- Does not transmit data externally

## Installation

```bash
cp -r examples/plugins/dns_query_logger/ plugins/
```

The plugin manager discovers plugins in the `plugins/` directory automatically at startup.

## Output

Logs appear in `~/.packetanalyzer/logs/app.log`:

```json
{"event": "dns_query", "plugin": "dns_query_logger", "qname": "example.com", "session_id": "abc123"}
```
