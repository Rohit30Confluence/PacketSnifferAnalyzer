# Deployment Guide

This guide covers deployment options for PacketSnifferAnalyzer.

---

## Deployment Modes

| Mode | Use Case | Complexity |
|---|---|---|
| Local CLI | Single analyst, command-line workflow | Low |
| Local GUI | Single analyst, graphical workflow | Low |
| Local Dashboard | Single analyst, browser-based workflow | Low |
| Docker | Isolated environment, reproducible setup | Medium |
| Server (headless) | Continuous monitoring, remote access | High |

---

## Local Installation

See [Installation Guide](../installation.md) for detailed instructions.

```bash
pip install packetsnifferanalyzer
sudo psa capture start --interface eth0
```

---

## Docker Deployment

### Development

```bash
git clone https://gitlab.com/dr-confluence-group/PacketSnifferAnalyzer.git
cd PacketSnifferAnalyzer
docker compose up -d
docker compose exec app psa interfaces
```

### Production (Headless Dashboard)

```bash
# Build the production image
docker build -f docker/Dockerfile --target production -t psa:latest .

# Run with NET_RAW capability
docker run -d \
  --name psa \
  --cap-add NET_RAW \
  --cap-add NET_ADMIN \
  --network host \
  -p 127.0.0.1:8080:8080 \
  -v psa-sessions:/home/psa/.packetanalyzer/sessions \
  -v psa-logs:/home/psa/.packetanalyzer/logs \
  psa:latest
```

**Security note:** `--network host` is required for interface access. The dashboard port is bound to `127.0.0.1` only.

---

## Environment Variables

All settings can be configured via environment variables prefixed with `PSA_`:

| Variable | Default | Description |
|---|---|---|
| `PSA_ENV` | `production` | Runtime environment |
| `PSA_LOG_LEVEL` | `INFO` | Log level |
| `PSA_LOG_DIR` | `~/.packetanalyzer/logs` | Log directory |
| `PSA_DATA_DIR` | `~/.packetanalyzer/sessions` | Session data directory |
| `PSA_DASHBOARD_HOST` | `127.0.0.1` | Dashboard bind host |
| `PSA_DASHBOARD_PORT` | `8080` | Dashboard port |
| `PSA_RING_BUFFER_SIZE` | `65536` | Capture ring buffer size |
| `PSA_PCAP_ROTATION_SIZE_MB` | `100` | PCAP rotation size |
| `PSA_PCAP_ROTATION_INTERVAL_HOURS` | `1` | PCAP rotation interval |

---

## Security Hardening for Production

1. **Never expose the dashboard externally** without a reverse proxy with authentication.
2. **Use encrypted sessions** for sensitive captures: `psa capture start --encrypt`.
3. **Review audit logs** regularly: `~/.packetanalyzer/logs/audit.log`.
4. **Pin the Docker image** to a specific digest in production.
5. **Run as non-root** in Docker (the production image uses the `psa` user).
6. **Restrict file permissions** on session data: `chmod 700 ~/.packetanalyzer/sessions`.
