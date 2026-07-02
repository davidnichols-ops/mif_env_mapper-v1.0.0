#!/usr/bin/env python3
"""
MIF Environment Mapper - CLI Entrypoint

Usage:
    python main.py                    # Output JSON to stdout
    python main.py --output FILE      # Write JSON to file
    python main.py --summary          # Output human-readable summary
    python main.py --verify           # Run verification mode
"""

import argparse
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mif_env_mapper.orchestrator import Orchestrator, OrchestrationError
from mif_env_mapper.reporter import Reporter


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="mif_env_mapper",
        description="Multi-Platform System Environment Mapping Engine"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output file path (default: stdout)"
    )
    
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Output human-readable summary instead of JSON"
    )
    
    parser.add_argument(
        "--compact", "-c",
        action="store_true",
        help="Output compact JSON (no indentation)"
    )
    
    parser.add_argument(
        "--verify", "-v",
        action="store_true",
        help="Run verification mode (validate pipeline without output)"
    )
    
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Subprocess timeout in seconds (default: 30)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser


def main() -> int:
    """Main CLI entrypoint."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator(
            timeout=args.timeout,
            pretty_output=not args.compact
        )
        reporter = Reporter(pretty=not args.compact)
        
        if args.verify:
            # Verification mode: run pipeline, confirm success
            print("[MIF] Running verification mode...")
            data = orchestrator.run_silent()
            print(f"[MIF] Verification successful!")
            print(f"[MIF] Platform: {data['system_metadata']['os_platform']}")
            print(f"[MIF] System packages: {len(data['packages']['system_level'])}")
            print(f"[MIF] Runtime packages: {len(data['packages']['language_runtimes'])}")
            print(f"[MIF] Duration: {orchestrator.duration_ms}ms")
            return 0
        
        # Run pipeline
        data = orchestrator.run_silent()
        
        # Output
        if args.output:
            with open(args.output, "w") as output_target:
                if args.summary:
                    reporter.write_summary(data, output_target)
                else:
                    reporter.write_json(data, output_target)
            print(f"[MIF] Output written to: {args.output}")
        else:
            if args.summary:
                reporter.write_summary(data, None)
            else:
                reporter.write_json(data, None)
        
        return 0
        
    except OrchestrationError as e:
        print(f"CRITICAL_PIPELINE_ERROR: {str(e)}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[MIF] Operation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"UNEXPECTED_ERROR: {str(e)}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
