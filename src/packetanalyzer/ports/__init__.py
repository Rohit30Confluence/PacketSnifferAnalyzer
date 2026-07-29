"""Port interfaces (abstract adapters) for PacketSnifferAnalyzer.

This package defines the abstract interfaces (ports) that separate the
domain and application layers from infrastructure concerns. All concrete
implementations live in the adapters/ package.

Following the Hexagonal Architecture pattern, the domain never depends
on concrete implementations — only on these abstract interfaces.
"""
