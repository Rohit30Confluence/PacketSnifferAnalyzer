"""Domain layer — pure Python domain models.

This package contains the core domain models for PacketSnifferAnalyzer.
It has zero dependencies on external libraries, UI frameworks, or
infrastructure concerns. All models are plain Python dataclasses.

Modules:
    packet: Packet and Layer domain models
    session: CaptureSession domain model
    flow: Flow and FlowTable domain models
    filter: FilterExpression domain model
    alert: AlertRule and AlertEvent domain models
    statistics: StatisticsSnapshot domain model
"""
