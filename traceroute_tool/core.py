import sys
import subprocess
import re
import json
from typing import List, Dict, Any, Callable, Optional

class Hop:
    def __init__(self, hop_number: int, host: str, ip: Optional[str], rtt_values: List[Any]):
        self.hop_number = hop_number
        self.host = host
        self.ip = ip
        self.rtt_values = rtt_values

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hop_number": self.hop_number,
            "host": self.host,
            "ip": self.ip,
            "rtt_values": self.rtt_values
        }

class TracerouteResult:
    def __init__(self, host: str, output: str, exit_code: int):
        self.host = host
        self.output = output
        self.exit_code = exit_code
        self.hops: List[Hop] = []
        self._parse_stats()

    def _parse_stats(self):
        self.hops = []
        lines = self.output.splitlines()
        for line in lines:
            match = re.match(r"^\s*(\d+)\s+([^\s]+)(?:\s+\(([^)]+)\))?\s+(.*)", line)
            if match:
                hop_num = int(match.group(1))
                host = match.group(2)
                ip = match.group(3) or host
                rest = match.group(4)
                
                rtt_matches = re.findall(r"([\d.]+)\s*ms", rest)
                rtt_values = [float(r) for r in rtt_matches]
                
                self.hops.append(Hop(hop_num, host, ip, rtt_values))

    @property
    def hops_count(self) -> int:
        return len(self.hops)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "host": self.host,
            "hops_count": self.hops_count,
            "hops": [h.to_dict() for h in self.hops],
            "exit_code": self.exit_code,
            "output": self.output
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


def build_traceroute_command(
    target: str,
    max_hops: Optional[int] = None,
    timeout: Optional[int] = None,
    no_dns: bool = False
) -> List[str]:
    is_windows = sys.platform.startswith("win")
    
    if is_windows:
        cmd = ["tracert"]
        if max_hops is not None:
            cmd.extend(["-h", str(max_hops)])
        if timeout is not None:
            cmd.extend(["-w", str(int(timeout * 1000))])
        if no_dns:
            cmd.append("-d")
    else:
        cmd = ["traceroute"]
        if max_hops is not None:
            cmd.extend(["-m", str(max_hops)])
        if timeout is not None:
            cmd.extend(["-w", str(timeout)])
        if no_dns:
            cmd.append("-n")

    cmd.append(target)
    return cmd


def execute_traceroute(
    target: str,
    max_hops: Optional[int] = None,
    timeout: Optional[int] = None,
    no_dns: bool = False,
    on_output: Optional[Callable[[str], None]] = None,
    verbose: bool = False
) -> TracerouteResult:
    cmd = build_traceroute_command(target, max_hops=max_hops, timeout=timeout, no_dns=no_dns)
    
    if verbose and on_output:
        on_output(f"Executing command: {' '.join(cmd)}")

    output_lines = []
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                cleaned_line = line.rstrip()
                output_lines.append(cleaned_line)
                if on_output:
                    on_output(cleaned_line)
                    
        return_code = process.wait()
    except Exception as e:
        err_msg = f"Error executing traceroute: {e}"
        output_lines.append(err_msg)
        if on_output:
            on_output(err_msg)
        return_code = 1

    full_output = "\n".join(output_lines)
    return TracerouteResult(host=target, output=full_output, exit_code=return_code)
