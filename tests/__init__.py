"""Test suite for PacketSnifferAnalyzer.

Test organization:
    unit/        — Unit tests (no external dependencies, fully mocked)
    integration/ — Integration tests (may use PCAP fixtures)
    e2e/         — End-to-end tests (full pipeline)
    fixtures/    — Shared test data (PCAP files, configs)

Markers:
    @pytest.mark.unit         — Unit test
    @pytest.mark.integration  — Integration test
    @pytest.mark.e2e          — End-to-end test
    @pytest.mark.slow         — Takes more than 5 seconds
    @pytest.mark.gui          — Requires a display (PyQt6)
    @pytest.mark.requires_root — Requires elevated privileges
"""
