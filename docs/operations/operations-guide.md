# Operations Guide

This guide covers day-to-day operational procedures for PacketSnifferAnalyzer.

---

## Daily Operations Checklist

- [ ] Check disk usage: `df -h ~/.packetanalyzer/`
- [ ] Review error log for new errors: `tail -20 ~/.packetanalyzer/logs/error.log`
- [ ] Review alert log for triggered alerts: `tail -20 ~/.packetanalyzer/logs/alerts.log`
- [ ] Verify active sessions are running as expected: `psa capture status`
- [ ] Archive or delete old sessions if disk usage is high

---

## Session Lifecycle

```
CREATED → RUNNING → PAUSED → RUNNING → STOPPED
                                              ↓
                                         [Archived / Deleted]
```

### Session Commands

```bash
# List all sessions
psa sessions list

# View session details
psa sessions show --session-id <id>

# Delete a session
psa sessions delete --session-id <id>

# Export a session
psa export --session <id> --format json --output results.json
```

---

## Log Rotation

Logs are rotated automatically:
- **App log:** 10 MB max, 30 backups
- **Error log:** 10 MB max, 30 backups
- **Audit log:** 10 MB max, 90 backups
- **Alert log:** 10 MB max, 90 backups

To manually rotate logs:
```bash
# Send SIGHUP to the process (if running as a daemon)
kill -HUP $(pgrep -f 'psa capture')
```

---

## Backup Procedures

### Session Data

```bash
# Backup all sessions
tar -czf psa-sessions-$(date +%Y%m%d).tar.gz ~/.packetanalyzer/sessions/

# Backup configuration
cp -r configs/ configs-backup-$(date +%Y%m%d)/
```

### Alert Rules

```bash
# Alert rules are YAML files — version control them
git add configs/alert_rules.yaml
git commit -m "chore: update alert rules"
```

---

## Upgrading

```bash
# 1. Stop any active captures
psa capture stop

# 2. Upgrade the package
pip install --upgrade packetsnifferanalyzer

# 3. Verify the upgrade
psa --version

# 4. Run the test suite
pytest tests/unit/ -q

# 5. Resume operations
sudo psa capture start --interface eth0
```

---

## Rollback Procedure

```bash
# Install a specific version
pip install packetsnifferanalyzer==1.0.0

# Verify
psa --version
```
