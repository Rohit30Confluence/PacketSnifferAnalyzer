#!/usr/bin/env bash
# scripts/generate-test-pcap.sh
#
# Generates synthetic PCAP fixtures for the test suite.
# Requires: tcpdump or scapy
#
# Usage: bash scripts/generate-test-pcap.sh

set -euo pipefail

FIXTURES_DIR="tests/fixtures"

echo "==> Generating test PCAP fixtures..."

mkdir -p "$FIXTURES_DIR"

# Generate a minimal valid PCAP file using Python/Scapy
python3 - <<'EOF'
from scapy.all import Ether, IP, TCP, UDP, DNS, DNSQR, wrpcap
from datetime import datetime

packets = []

# TCP SYN packet
pkt1 = Ether(src="aa:bb:cc:dd:ee:01", dst="aa:bb:cc:dd:ee:02") / \
       IP(src="192.168.1.100", dst="8.8.8.8", ttl=64) / \
       TCP(sport=54321, dport=443, flags="S", seq=1000)
packets.append(pkt1)

# TCP SYN-ACK
pkt2 = Ether(src="aa:bb:cc:dd:ee:02", dst="aa:bb:cc:dd:ee:01") / \
       IP(src="8.8.8.8", dst="192.168.1.100", ttl=128) / \
       TCP(sport=443, dport=54321, flags="SA", seq=2000, ack=1001)
packets.append(pkt2)

# UDP DNS query
pkt3 = Ether(src="aa:bb:cc:dd:ee:01", dst="aa:bb:cc:dd:ee:02") / \
       IP(src="192.168.1.100", dst="8.8.8.8") / \
       UDP(sport=12345, dport=53) / \
       DNS(rd=1, qd=DNSQR(qname="example.com"))
packets.append(pkt3)

wrpcap("tests/fixtures/sample.pcap", packets)
print(f"Generated tests/fixtures/sample.pcap with {len(packets)} packets")
EOF

# Generate a malformed PCAP (truncated packet)
python3 - <<'EOF'
import struct

# Write a valid PCAP global header
with open("tests/fixtures/malformed.pcap", "wb") as f:
    # PCAP global header
    f.write(struct.pack("<IHHiIII",
        0xa1b2c3d4,  # magic number
        2, 4,        # version
        0,           # timezone
        0,           # timestamp accuracy
        65535,       # snaplen
        1,           # link type (Ethernet)
    ))
    # Write a packet record with truncated data
    f.write(struct.pack("<IIII",
        0,    # timestamp seconds
        0,    # timestamp microseconds
        100,  # captured length (claims 100 bytes)
        100,  # original length
    ))
    # Write only 20 bytes (truncated)
    f.write(b"\x00" * 20)

print("Generated tests/fixtures/malformed.pcap")
EOF

echo "==> Test fixtures generated successfully."
echo "    tests/fixtures/sample.pcap"
echo "    tests/fixtures/malformed.pcap"
