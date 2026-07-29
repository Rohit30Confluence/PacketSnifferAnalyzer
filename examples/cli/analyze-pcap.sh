#!/usr/bin/env bash
# examples/cli/analyze-pcap.sh
#
# Demonstrates offline PCAP analysis using the PSA CLI.
# Analyzes a PCAP file and exports statistics and flows.
#
# Usage: bash examples/cli/analyze-pcap.sh <path-to-pcap>

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "Usage: $0 <path-to-pcap>"
    exit 1
fi

PCAP_FILE="$1"
OUTPUT_DIR="./analysis-output"

mkdir -p "$OUTPUT_DIR"

echo "==> Analyzing: $PCAP_FILE"
echo ""

# Show statistics
echo "--- Traffic Statistics ---"
psa analyze --file "$PCAP_FILE" --stats

echo ""
echo "--- Active Flows ---"
psa analyze --file "$PCAP_FILE" --flows

# Export to multiple formats
echo ""
echo "==> Exporting to JSON (with payload redaction)..."
psa export \
  --session "$PCAP_FILE" \
  --format json \
  --output "$OUTPUT_DIR/analysis.json" \
  --redact-payload

echo "==> Exporting to CSV..."
psa export \
  --session "$PCAP_FILE" \
  --format csv \
  --output "$OUTPUT_DIR/analysis.csv"

echo ""
echo "==> Analysis complete."
echo "    JSON: $OUTPUT_DIR/analysis.json"
echo "    CSV:  $OUTPUT_DIR/analysis.csv"
