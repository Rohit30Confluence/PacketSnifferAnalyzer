# Runbook: Capture Session Management

**Version:** 1.0
**Audience:** Operators and network analysts
**Last Updated:** 2026-07-29

---

## Overview

This runbook covers the operational procedures for managing packet capture sessions in PacketSnifferAnalyzer.

---

## Starting a Capture Session

### Prerequisites

- [ ] Verify you have legal authorization to capture traffic on the target network
- [ ] Verify sufficient disk space: `df -h ~/.packetanalyzer/sessions`
- [ ] Verify the target interface is up: `psa interfaces`
- [ ] Verify privileges: `psa capture status`

### Procedure

```bash
# 1. List available interfaces
psa interfaces

# 2. Start capture with appropriate filter
sudo psa capture start \
  --interface eth0 \
  --filter "tcp port 443" \
  --name "investigation-$(date +%Y%m%d-%H%M%S)" \
  --output /path/to/output.pcap

# 3. Verify capture is running
psa capture status

# 4. Monitor statistics
watch -n 1 psa capture status --json
```

### Expected Output

```
Session: investigation-20240115-103000
State:   RUNNING
Interface: eth0
Filter:  tcp port 443
Packets: 1,234
Dropped: 0
Duration: 00:02:15
```

---

## Stopping a Capture Session

```bash
# Stop the active session
psa capture stop

# Verify the session was saved
psa sessions list
```

---

## Handling High Drop Rates

**Threshold:** Alert if drop rate exceeds 0.1% of total packets.

**Immediate actions:**

1. Apply a more specific BPF filter to reduce capture volume:
   ```bash
   # Instead of capturing all traffic:
   sudo psa capture start -i eth0
   # Capture only the traffic you need:
   sudo psa capture start -i eth0 -f "tcp and host 10.0.0.1"
   ```

2. Increase the ring buffer size:
   ```bash
   PSA_RING_BUFFER_SIZE=131072 sudo psa capture start -i eth0
   ```

3. Move PCAP output to a faster disk (SSD preferred).

4. Reduce the number of active plugins.

---

## Disk Space Management

**Monitor disk usage:**
```bash
du -sh ~/.packetanalyzer/sessions/
df -h ~/.packetanalyzer/
```

**PCAP rotation** is automatic (default: 100 MB or 1 hour). Configure with:
```bash
PSA_PCAP_ROTATION_SIZE_MB=50 psa capture start ...
PSA_PCAP_ROTATION_INTERVAL_HOURS=2 psa capture start ...
```

**Delete old sessions:**
```bash
psa sessions list
psa sessions delete --session-id <id>
```

---

## Recovering from a Crash

If PacketSnifferAnalyzer crashes during capture:

1. Check the error log:
   ```bash
   tail -50 ~/.packetanalyzer/logs/error.log
   ```

2. Check the audit log for the last session:
   ```bash
   tail -10 ~/.packetanalyzer/logs/audit.log | python -m json.tool
   ```

3. Attempt to recover the PCAP file:
   ```bash
   psa analyze --file ~/.packetanalyzer/sessions/<session-id>/*.pcap
   ```
   The tool will detect truncation and recover valid packets.

4. Report the crash with the error log: [Bug Report](https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer/-/issues/new?issuable_template=bug_report)
