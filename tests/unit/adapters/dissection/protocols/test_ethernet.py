from scapy.all import Ether, IP

from packetanalyzer.adapters.dissection.protocols.ethernet import (
    dissect_ethernet,
)


def test_dissect_ethernet() -> None:
    packet = Ether(
        src="aa:bb:cc:dd:ee:ff",
        dst="11:22:33:44:55:66",
    ) / IP(dst="8.8.8.8")

    layer = dissect_ethernet(packet)

    assert layer.protocol == "Ethernet"
    assert layer.fields["src"] == "aa:bb:cc:dd:ee:ff"
    assert layer.fields["dst"] == "11:22:33:44:55:66"
    assert layer.fields["type"] == 0x0800
    assert layer.raw_bytes == bytes(packet)


def test_dissect_ethernet_rejects_invalid_layer() -> None:
    try:
        dissect_ethernet(object())
    except TypeError as exc:
        assert "Invalid Scapy Ethernet layer" in str(exc)
    else:
        raise AssertionError("Expected TypeError")
