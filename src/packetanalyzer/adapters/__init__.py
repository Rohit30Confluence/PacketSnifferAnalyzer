"""Adapter implementations for PacketSnifferAnalyzer.

This package contains concrete implementations of the port interfaces
defined in packetanalyzer.ports. Each sub-package corresponds to a
specific infrastructure concern.

Sub-packages:
    capture: Packet capture backends (Scapy, PCAP file)
    dissection: Protocol dissection backends
    storage: Session and packet storage backends
    notification: Alert notification backends
"""
