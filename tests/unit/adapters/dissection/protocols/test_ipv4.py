from scapy.all import IP, TCP

from packetanalyzer.adapters.dissection.protocols.ipv4 import dissect_ipv4


def test_dissect_ipv4() -> None:
    packet = IP(
        src="192.168.1.100",
        dst="8.8.8.8",
        ttl=64,
    ) / TCP(dport=443)

    layer = dissect_ipv4(packet)

    assert layer.protocol == "IPv4"
    assert layer.fields["version"] == 4
    assert layer.fields["ihl"] == 5
    assert layer.fields["ttl"] == 64
    assert layer.fields["proto"] == 6
    assert layer.fields["src"] == "192.168.1.100"
    assert layer.fields["dst"] == "8.8.8.8"
    assert layer.raw_bytes == bytes(packet)


def test_dissect_ipv4_rejects_invalid_layer() -> None:
    try:
        dissect_ipv4(object())
    except TypeError as exc:
        assert "Invalid Scapy IPv4 layer" in str(exc)
    else:
        raise AssertionError("Expected TypeError")
