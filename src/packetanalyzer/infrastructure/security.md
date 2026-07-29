# Security Model

This document describes the security architecture, threat model, and security controls implemented in PacketSnifferAnalyzer.

---

## Security Principles

1. **Minimum privilege:** The tool requests only the privileges it needs and drops them as soon as possible.
2. **No exfiltration by default:** Captured data never leaves the local machine without explicit user action.
3. **Defense in depth:** Multiple layers of controls protect against misuse.
4. **Transparency:** All security-relevant actions are recorded in the audit log.
5. **Ethical design:** The tool is designed for network observability, not credential harvesting.

---

## Threat Model

### In Scope

| Threat | Control |
|---|---|
| Unauthorized use on foreign networks | Legal notice on first run; documentation |
| Credential extraction via the tool | SR-10: No credential-highlighting features |
| Data exfiltration via dashboard | Dashboard binds to 127.0.0.1 by default |
| Malicious plugin loading | Plugin validation; error isolation |
| Sensitive data in logs | Payloads never written to logs |
| Dependency vulnerabilities | pip-audit in CI; pinned dependencies |
| Path traversal via file inputs | Input validation and sanitization |
| Insecure webhook URLs | HTTPS-only webhook validation |
| Unencrypted session files | AES-256-GCM optional encryption |

### Out of Scope

- Physical access to the host machine
- Compromise of the OS or kernel
- Attacks against the network being monitored
- Social engineering of the operator

---

## Privilege Model

### Linux

Required capabilities: `CAP_NET_RAW`, `CAP_NET_ADMIN`

Process:
1. Tool starts with elevated privileges (sudo or capabilities)
2. Interface is bound
3. Privileges are dropped to minimum required level
4. Capture proceeds with reduced privilege

### macOS

Root access required. No capability drop mechanism available.

### Windows

Administrator access required. Npcap driver handles privilege separation.

---

## Data Boundaries

```
┌───────────────────────────────────────────────────────────┐
│                    LOCAL MACHINE                          │
│                                                           │
│  Network Interface → Capture Engine → Dissection Engine   │
│                                          │                │
│                              ┌──────────┴─────────┐       │
│                              │ Payload stays here │       │
│                              └───────────────────┘       │
│                                                           │
│  Logs: metadata only (no payload)                         │
│  Dashboard: metadata only (127.0.0.1 only by default)     │
│  Exports: optional payload redaction                      │
│                                                           │
│  ───────────────────────────────────────────────────────  │
│  EXTERNAL BOUNDARY: Only crossed by explicit user action   │
│  (export to file, webhook alert, PCAP share)              │
└───────────────────────────────────────────────────────────┘
```

---

## Encryption

Session files can be encrypted with AES-256-GCM:

- **Algorithm:** AES-256-GCM (authenticated encryption)
- **Key derivation:** Argon2id with random salt
- **Parameters:** time_cost=3, memory_cost=65536, parallelism=4
- **Key storage:** Keys are never stored; derived from passphrase on each access

---

## Audit Log

All security-relevant events are recorded in `~/.packetanalyzer/logs/audit.log`:

- Session start and stop (with interface, filter, operator, version)
- Filter changes
- Export actions (format, destination, packet count)
- Alert triggers
- Legal notice acceptance

The audit log is append-only and never contains packet payload data.

---

## Dependency Security

- All dependencies are pinned to exact versions
- `pip-audit` runs on every CI pipeline to detect CVEs
- `bandit` performs SAST on every CI pipeline
- License compliance is checked to prevent GPL-incompatible dependencies

---

## Reporting Vulnerabilities

See [SECURITY.md](../SECURITY.md) for the responsible disclosure policy.
