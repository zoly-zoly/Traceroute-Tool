import sys
import pytest
from traceroute_tool.core import build_traceroute_command, TracerouteResult

def test_build_traceroute_command_linux(monkeypatch):
    monkeypatch.setattr(sys, "platform", "linux")
    cmd = build_traceroute_command("127.0.0.1", max_hops=10, timeout=2, no_dns=True)
    assert cmd == ["traceroute", "-m", "10", "-w", "2", "-n", "127.0.0.1"]

def test_build_traceroute_command_windows(monkeypatch):
    monkeypatch.setattr(sys, "platform", "win32")
    cmd = build_traceroute_command("127.0.0.1", max_hops=15, timeout=3, no_dns=True)
    assert cmd == ["tracert", "-h", "15", "-w", "3000", "-d", "127.0.0.1"]

def test_traceroute_result_parsing():
    sample_output = """traceroute to 127.0.0.1 (127.0.0.1), 30 hops max, 60 byte packets
 1  localhost (127.0.0.1)  0.035 ms  0.021 ms  0.018 ms"""

    result = TracerouteResult("127.0.0.1", sample_output, 0)
    assert result.hops_count == 1
    assert result.hops[0].hop_number == 1
    assert result.hops[0].host == "localhost"
    assert result.hops[0].ip == "127.0.0.1"
    assert result.hops[0].rtt_values == [0.035, 0.021, 0.018]

    d = result.to_dict()
    assert d["host"] == "127.0.0.1"
    assert d["hops_count"] == 1
    assert len(d["hops"]) == 1
    
    j = result.to_json()
    assert "localhost" in j
