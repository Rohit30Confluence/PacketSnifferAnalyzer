from scapy.all import IP, TCP

from packetanalyzer.adapters.dissection.protocols.tcp import dissect_tcp


def test_dissect_tcp() -> None:
    packet = TCP(
        sport=54321,
        dport=443,
        seq=1000,
        ack=2000,
        flags="S",
        window=65535,
    )

    layer = dissect_tcp(packet)

    assert layer.protocol == "TCP"
    assert layer.fields["sport"] == 54321
    assert layer.fields["dport"] == 443
    assert layer.fields["seq"] == 1000
    assert layer.fields["ack"] == 2000
    assert layer.fields["flags"] == "S"
    assert layer.fields["window"] == 65535
    assert layer.fields["data_offset"] == 5
    assert layer.raw_bytes == bytes(packet)


def test_dissect_tcp_rejects_invalid_layer() -> None:
    try:
        dissect_tcp(object())
    except TypeError as exc:
        assert "Invalid Scapy TCP layer" in str(exc)
    else:
        raise AssertionError("Expected TypeError")
