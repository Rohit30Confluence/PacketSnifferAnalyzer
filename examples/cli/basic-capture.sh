#!/usr/bin/env bash
# examples/cli/basic-capture.sh
#
# Demonstrates a basic packet capture workflow using the PSA CLI.
# This script captures HTTPS traffic for 60 seconds and exports to JSON.
#
# Prerequisites:
#   - PacketSnifferAnalyzer installed
#   - Sufficient privileges (run with sudo on Linux/macOS)
#   - Replace INTERFACE with your actual interface name

set -euo pipefail

INTERFACE="eth0"  # Change this to your interface
SESSION_NAME="example-$(date +%Y%m%d-%H%M%S)"
OUTPUT_DIR="./example-output"

mkdir -p "$OUTPUT_DIR"

echo "==> Starting HTTPS traffic capture on $INTERFACE for 60 seconds..."
echo "    Session: $SESSION_NAME"
echo ""

# Start capture in background
psa capture start \
  --interface "$INTERFACE" \
  --filter "tcp port 443" \
  --name "$SESSION_NAME" \
  --output "$OUTPUT_DIR/$SESSION_NAME.pcap" &

CAPTURE_PID=$!

# Wait 60 seconds
sleep 60

# Stop capture
psa capture stop

wait $CAPTURE_PID 2>/dev/null || true

echo ""
echo "==> Capture complete. Exporting to JSON..."

psa export \
  --session "$SESSION_NAME" \
  --format json \
  --output "$OUTPUT_DIR/$SESSION_NAME.json" \
  --redact-payload

echo "==> Export complete."
echo "    PCAP: $OUTPUT_DIR/$SESSION_NAME.pcap"
echo "    JSON: $OUTPUT_DIR/$SESSION_NAME.json"
