"""PacketSnifferAnalyzer — Python-based packet sniffer and traffic analyzer.

This package provides:
- Live packet capture from network interfaces
- Protocol dissection (Ethernet, IP, TCP, UDP, DNS, TLS, and more)
- BPF pre-capture filtering and display post-capture filtering
- Real-time traffic statistics and flow tracking
- Session management with PCAP save/load
- Export to PCAP, JSON, CSV, and plain-text formats
- Alert engine with threshold-based rules
- Plugin system for custom dissectors
- Three interface modes: CLI, desktop GUI, and web dashboard

Legal Notice:
    Packet capture on a network you do not own or have explicit written
    authorization to monitor may violate applicable laws. Users are solely
    responsible for compliance with applicable laws and regulations.
"""

from __future__ import annotations

__version__ = "0.1.0-alpha.1"
__author__ = "Dr.Confluence-group"
__license__ = "Unlicense"
