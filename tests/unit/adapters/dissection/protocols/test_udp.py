from scapy.all import UDP

from packetanalyzer.adapters.dissection.protocols.udp import dissect_udp


def test_dissect_udp() -> None:
    packet = UDP(
        sport=5353,
        dport=53,
    )

    layer = dissect_udp(packet)

    assert layer.protocol == "UDP"
    assert layer.fields["sport"] == 5353
    assert layer.fields["dport"] == 53
    assert layer.fields["length"] == 8
    assert isinstance(layer.fields["checksum"], int)
    assert layer.raw_bytes == bytes(packet)


def test_dissect_udp_rejects_invalid_layer() -> None:
    try:
        dissect_udp(object())
    except TypeError as exc:
        assert "Invalid Scapy UDP layer" in str(exc)
    else:
        raise AssertionError("Expected TypeError")
