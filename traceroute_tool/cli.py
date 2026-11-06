import argparse
import sys
from traceroute_tool.core import execute_traceroute, TracerouteResult

def main():
    parser = argparse.ArgumentParser(
        description="A robust, cross-platform Python CLI traceroute utility with real-time hop streaming and JSON export."
    )
    parser.add_argument("target", help="Target host or IP address to trace")
    parser.add_argument("-m", "--max-hops", type=int, default=None, help="Maximum number of hops")
    parser.add_argument("-w", "--timeout", type=int, default=None, help="Timeout in seconds per hop probe")
    parser.add_argument("-n", "--no-dns", action="store_true", help="Do not resolve IP addresses to hostnames")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    output_lines = []

    def handle_output(line: str):
        if not args.json:
            print(line)
            sys.stdout.flush()
        output_lines.append(line)

    try:
        result = execute_traceroute(
            target=args.target,
            max_hops=args.max_hops,
            timeout=args.timeout,
            no_dns=args.no_dns,
            on_output=handle_output,
            verbose=args.verbose
        )
        if args.json:
            print(result.to_json())
        sys.exit(result.exit_code)
    except KeyboardInterrupt:
        if not args.json:
            print("\n--- Traceroute statistics (Interrupted) ---")
            full_output = "\n".join(output_lines)
            partial_result = TracerouteResult(host=args.target, output=full_output, exit_code=0)
            print(f"Hops traced before interruption: {partial_result.hops_count}")
        else:
            full_output = "\n".join(output_lines)
            partial_result = TracerouteResult(host=args.target, output=full_output, exit_code=0)
            print(partial_result.to_json())
        sys.exit(0)

if __name__ == "__main__":
    main()
