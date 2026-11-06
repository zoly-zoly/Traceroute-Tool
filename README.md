# Py Traceroute Tool (`py-traceroute-tool`)

[![CI](https://github.com/username/py-traceroute-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/username/py-traceroute-tool/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

A robust, cross-platform Python CLI traceroute utility that streams network hops in real-time, parses route metrics, exports JSON, and runs seamlessly across **Linux, macOS, and Windows**.

---

## Features

- **Real-Time Hop Streaming**: Streams hop responses live to the terminal as route probes return.
- **Cross-Platform**: Automatically uses platform-native syntax (`traceroute` on Unix, `tracert` on Windows).
- **JSON Output Mode (`--json`)**: Export structured route data and hop metrics for automation and network diagnostics.
- **Verbose Logging (`-v`)**: Display underlying command execution details.
- **Zero Heavy Dependencies**: Built purely on standard library primitives (`subprocess`, `argparse`, `re`, `json`).
- **CLI & API Ready**: Can be invoked via command line (`py-traceroute`) or imported as a Python package.

---

## Installation

Clone the repository and install it locally using `pip`:

```bash
git clone https://github.com/zoly-zoly/Traceroute-Tool.git
cd py-traceroute-tool
pip install .
```

For development (including testing tools):
```bash
pip install -e .[dev]
```

---

## Usage

### Command Line Interface

```bash
# Trace route to a destination
py-traceroute google.com

# Trace with maximum hops limit
py-traceroute 8.8.8.8 -m 15

# Output results as structured JSON
py-traceroute 1.1.1.1 --json

# Enable verbose logging
py-traceroute localhost -v
```

### Python API

```python
from traceroute_tool.core import execute_traceroute

# Define a real-time output callback
def handle_line(line):
    print(f"[HOP] {line}")

# Execute traceroute
result = execute_traceroute("127.0.0.1", max_hops=10, on_output=handle_line)

print(f"Total Hops Traced: {result.hops_count}")
print(result.to_json(indent=2))
```

---

## Running Tests

Run unit tests with `pytest`:

```bash
pytest
```

---

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
