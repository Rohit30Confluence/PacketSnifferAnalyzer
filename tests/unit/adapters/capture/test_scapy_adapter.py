"""Unit tests for the Scapy capture adapter."""

from __future__ import annotations

from datetime import datetime, timezone
from threading import Event
from unittest.mock import MagicMock, patch

from scapy.all import Ether, IP, TCP
from scapy.interfaces import NetworkInterface

from packetanalyzer.adapters.capture.scapy_adapter import ScapyCaptureAdapter
from packetanalyzer.domain.packet import Packet
from packetanalyzer.domain.session import CaptureSession, SessionState


class FakeFlags:
    def __init__(self, values: set[str]) -> None:
        self.values = values

    def __and__(self, value: str) -> bool:
        return value in self.values


class FakeDissector:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def dissect(
        self,
        raw: bytes,
        session_id: str,
        packet_id: int,
        interface: str,
    ) -> Packet:
        self.calls.append(
            {
                "raw": raw,
                "session_id": session_id,
                "packet_id": packet_id,
                "interface": interface,
            }
        )

        return Packet(
            packet_id=packet_id,
            timestamp=datetime.now(timezone.utc),
            interface=interface,
            length=len(raw),
            captured_length=len(raw),
            layers=(),
            raw_bytes=raw,
            session_id=session_id,
            parse_error=None,
        )


def make_interface(
    name: str,
    *,
    description: str = "",
    flags: set[str] | None = None,
    ips: dict[int, list[str]] | None = None,
) -> MagicMock:
    interface = MagicMock(spec=NetworkInterface)
    interface.name = name
    interface.description = description
    interface.flags = FakeFlags(flags or {"UP"})
    interface.ips = ips or {}
    return interface


def make_session(
    interface: str = "en0",
    *,
    bpf_filter: str = "",
) -> CaptureSession:
    return CaptureSession(
        session_id="test-session",
        name="Test Capture",
        interface=interface,
        bpf_filter=bpf_filter,
    )


def wait_until(predicate, timeout: float = 2.0) -> None:
    event = Event()

    def watcher() -> None:
        while not predicate():
            event.wait(0.01)
        event.set()

    import threading

    thread = threading.Thread(target=watcher, daemon=True)
    thread.start()

    assert event.wait(timeout), "condition was not reached"


class TestScapyCaptureAdapter:
    def test_interface_discovery_filters_unspecified_addresses(self) -> None:
        interface = make_interface(
            "en0",
            description="Wi-Fi",
            flags={"UP"},
            ips={
                4: ["0.0.0.0", "192.168.1.10"],
                6: ["::", "fe80::1234"],
            },
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=[interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert result[0].name == "en0"
        assert result[0].description == "Wi-Fi"
        assert result[0].is_up is True
        assert result[0].is_loopback is False
        assert result[0].addresses == [
            "192.168.1.10",
            "fe80::1234",
        ]

    def test_interface_discovery_detects_loopback(self) -> None:
        interface = make_interface(
            "lo0",
            flags={"UP", "LOOPBACK"},
            ips={4: ["127.0.0.1"], 6: ["::1"]},
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=[interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert result[0].is_up is True
        assert result[0].is_loopback is True
        assert result[0].addresses == [
            "127.0.0.1",
            "::1",
        ]

    def test_non_network_entries_are_ignored(self) -> None:
        interface = make_interface(
            "en0",
            ips={4: ["192.168.1.10"]},
        )

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.values",
            return_value=["invalid", interface],
        ):
            result = ScapyCaptureAdapter().list_interfaces()

        assert len(result) == 1
        assert result[0].name == "en0"

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_start_creates_capture_and_processing_workers(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()
        started = Event()
        release = Event()

        def fake_sniff(**_kwargs: object) -> None:
            started.set()
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        adapter = ScapyCaptureAdapter(FakeDissector())
        session = make_session()

        adapter.start(session, MagicMock())

        assert started.wait(1)
        assert session.state == SessionState.RUNNING
        assert adapter._capture_worker is not None
        assert adapter._processing_worker is not None
        assert adapter._capture_worker.is_alive()
        assert adapter._processing_worker.is_alive()

        release.set()
        adapter.stop()

        assert session.state == SessionState.STOPPED
        assert adapter._capture_worker is None
        assert adapter._processing_worker is None

    def test_start_rejects_missing_interface(self) -> None:
        adapter = ScapyCaptureAdapter()

        with patch(
            "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name",
            side_effect=KeyError("missing"),
        ):
            try:
                adapter.start(make_session("missing"), MagicMock())
            except ValueError as exc:
                assert "does not exist" in str(exc)
            else:
                raise AssertionError("ValueError expected")

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_bpf_filter_is_forwarded(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()
        started = Event()
        release = Event()

        def fake_sniff(**kwargs: object) -> None:
            assert kwargs["iface"] == "en0"
            assert kwargs["filter"] == "tcp port 443"
            assert kwargs["store"] is False
            assert callable(kwargs["prn"])
            started.set()
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        adapter = ScapyCaptureAdapter(FakeDissector())
        adapter.start(
            make_session(bpf_filter="tcp port 443"),
            MagicMock(),
        )

        assert started.wait(1)
        release.set()
        adapter.stop()

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_empty_filter_is_none(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()

        adapter = ScapyCaptureAdapter(FakeDissector())
        adapter.start(make_session(), MagicMock())
        adapter.stop()

        assert mock_sniff.call_args.kwargs["filter"] is None

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_packet_reaches_domain_callback(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()

        callback = MagicMock()
        delivered = Event()

        def callback_wrapper(packet: Packet) -> None:
            callback(packet)
            delivered.set()

        packet = Ether() / IP() / TCP()
        release = Event()

        def fake_sniff(**kwargs: object) -> None:
            kwargs["prn"](packet)
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        dissector = FakeDissector()
        adapter = ScapyCaptureAdapter(dissector)
        session = make_session()

        adapter.start(session, callback_wrapper)

        assert delivered.wait(2)
        callback.assert_called_once()

        domain_packet = callback.call_args.args[0]

        assert isinstance(domain_packet, Packet)
        assert domain_packet.packet_id == 1
        assert domain_packet.session_id == "test-session"
        assert domain_packet.interface == "en0"
        assert domain_packet.length == len(bytes(packet))

        release.set()
        adapter.stop()

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_statistics_and_packet_ids_are_updated(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()

        packets = [
            Ether() / IP() / TCP(),
            Ether() / IP() / TCP(),
        ]

        processed = Event()
        release = Event()

        def fake_sniff(**kwargs: object) -> None:
            kwargs["prn"](packets[0])
            kwargs["prn"](packets[1])
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        callback = MagicMock(
            side_effect=lambda _packet: (
                processed.set()
                if callback.call_count >= 2
                else None
            )
        )

        dissector = FakeDissector()
        adapter = ScapyCaptureAdapter(dissector)
        session = make_session()

        adapter.start(session, callback)

        wait_until(lambda: callback.call_count == 2)

        assert session.packet_count == 2
        assert session.byte_count == sum(
            len(bytes(packet)) for packet in packets
        )
        assert [call["packet_id"] for call in dissector.calls] == [1, 2]

        release.set()
        adapter.stop()

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_callback_failure_increments_drop_count(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()

        release = Event()

        def fake_sniff(**kwargs: object) -> None:
            kwargs["prn"](Ether() / IP() / TCP())
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        callback = MagicMock(
            side_effect=RuntimeError("downstream failure")
        )

        adapter = ScapyCaptureAdapter(FakeDissector())
        session = make_session()

        adapter.start(session, callback)

        wait_until(lambda: adapter.get_drop_count() == 1)

        assert session.drop_count == 1

        release.set()
        adapter.stop()

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_paused_packets_are_discarded(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()

        started = Event()
        release = Event()
        captured: dict[str, object] = {}

        def fake_sniff(**kwargs: object) -> None:
            captured["prn"] = kwargs["prn"]
            started.set()
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        callback = MagicMock()
        adapter = ScapyCaptureAdapter(FakeDissector())
        session = make_session()

        adapter.start(session, callback)
        assert started.wait(1)

        adapter.pause()

        captured["prn"](Ether() / IP() / TCP())
        assert callback.call_count == 0
        assert session.packet_count == 0
        assert adapter.get_drop_count() == 0

        adapter.resume()

        captured["prn"](Ether() / IP() / TCP())

        wait_until(lambda: callback.call_count == 1)

        assert session.packet_count == 1
        assert adapter.get_drop_count() == 0

        release.set()
        adapter.stop()

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_duplicate_start_is_rejected(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()

        started = Event()
        release = Event()

        def fake_sniff(**_kwargs: object) -> None:
            started.set()
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        adapter = ScapyCaptureAdapter(FakeDissector())
        adapter.start(make_session(), MagicMock())

        assert started.wait(1)

        try:
            adapter.start(make_session(), MagicMock())
        except RuntimeError as exc:
            assert "already running" in str(exc)
        else:
            raise AssertionError("RuntimeError expected")

        release.set()
        adapter.stop()

    def test_stop_without_capture_is_safe(self) -> None:
        adapter = ScapyCaptureAdapter()
        adapter.stop()
        assert adapter.get_drop_count() == 0

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_capture_worker_failure_sets_error(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()
        mock_sniff.side_effect = RuntimeError("capture failure")

        adapter = ScapyCaptureAdapter(FakeDissector())
        session = make_session()

        adapter.start(session, MagicMock())

        wait_until(lambda: session.state == SessionState.ERROR)

        adapter.stop()

        assert session.state == SessionState.ERROR

    @patch(
        "packetanalyzer.adapters.capture.scapy_adapter.conf.ifaces.dev_from_name"
    )
    @patch("packetanalyzer.adapters.capture.scapy_adapter.sniff")
    def test_stop_is_idempotent(
        self,
        mock_sniff: MagicMock,
        mock_interface: MagicMock,
    ) -> None:
        mock_interface.return_value = MagicMock()
        release = Event()

        def fake_sniff(**_kwargs: object) -> None:
            release.wait(2)

        mock_sniff.side_effect = fake_sniff

        adapter = ScapyCaptureAdapter(FakeDissector())
        session = make_session()

        adapter.start(session, MagicMock())
        release.set()

        adapter.stop()
        adapter.stop()

        assert session.state == SessionState.STOPPED
