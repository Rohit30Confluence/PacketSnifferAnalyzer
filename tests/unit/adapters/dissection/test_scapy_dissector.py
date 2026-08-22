from scapy.all import Ether, IP, TCP, UDP

from packetanalyzer.adapters.dissection.scapy_dissector import ScapyDissector


def test_dissect_ethernet_ipv4_tcp_packet() -> None:
    packet = (
        Ether(
            src="aa:bb:cc:dd:ee:ff",
            dst="11:22:33:44:55:66",
        )
        / IP(
            src="192.168.1.100",
            dst="8.8.8.8",
            ttl=64,
        )
        / TCP(
            sport=54321,
            dport=443,
            seq=1000,
            ack=2000,
            flags="S",
            window=65535,
        )
    )

    raw = bytes(packet)

    result = ScapyDissector().dissect(
        raw=raw,
        session_id="session-001",
        packet_id=1,
        interface="en0",
    )

    assert result.packet_id == 1
    assert result.session_id == "session-001"
    assert result.interface == "en0"
    assert result.length == len(raw)
    assert result.captured_length == len(raw)
    assert result.raw_bytes == raw
    assert result.parse_error is None

    assert [layer.protocol for layer in result.layers] == [
        "Ethernet",
        "IPv4",
        "TCP",
    ]

    assert result.get_layer("Ethernet") is not None
    assert result.get_layer("IPv4") is not None
    assert result.get_layer("TCP") is not None

    assert result.get_layer("IPv4").fields["src"] == "192.168.1.100"
    assert result.get_layer("IPv4").fields["dst"] == "8.8.8.8"
    assert result.get_layer("TCP").fields["sport"] == 54321
    assert result.get_layer("TCP").fields["dport"] == 443


def test_dissect_empty_packet_returns_parse_error() -> None:
    result = ScapyDissector().dissect(
        raw=b"",
        session_id="session-002",
        packet_id=2,
        interface="en0",
    )

    assert result.packet_id == 2
    assert result.session_id == "session-002"
    assert result.layers == ()
    assert result.parse_error == "Packet dissection failed: Empty packet data"
    assert result.length == 0
    assert result.captured_length == 0

def test_dissect_ethernet_ipv4_udp_packet() -> None:
    packet = (
        Ether(
            src="aa:bb:cc:dd:ee:ff",
            dst="11:22:33:44:55:66",
        )
        / IP(
            src="192.168.1.100",
            dst="8.8.8.8",
            ttl=64,
        )
        / UDP(
            sport=5353,
            dport=53,
        )
    )

    raw = bytes(packet)

    result = ScapyDissector().dissect(
        raw=raw,
        session_id="session-003",
        packet_id=3,
        interface="en0",
    )

    assert result.parse_error is None

    assert [layer.protocol for layer in result.layers] == [
        "Ethernet",
        "IPv4",
        "UDP",
    ]

    udp = result.get_layer("UDP")

    assert udp is not None
    assert udp.fields["sport"] == 5353
    assert udp.fields["dport"] == 53
