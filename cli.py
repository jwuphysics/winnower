#!/usr/bin/env python3
"""Command-line interface for The Winnower."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import WinnowerProcessor
from .config import load_config


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="winnower",
        description="Extract core technical details from research papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  winnower paper.pdf
  winnower https://arxiv.org/abs/2301.00001
  winnower 2301.00001
  winnower /path/to/papers/ --recursive
        """,
    )
    
    parser.add_argument(
        "input",
        help="Paper input: file path, directory, URL, or arXiv ID",
    )
    
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output directory (default: current directory)",
        default=Path.cwd(),
    )
    
    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Process directory recursively",
    )
    
    parser.add_argument(
        "--config",
        type=Path,
        help="Configuration file path",
    )
    
    parser.add_argument(
        "--model",
        choices=["openai", "anthropic"],
        default="openai",
        help="AI model provider (default: openai)",
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__import__('winnower').__version__}",
    )
    
    return parser


def main(argv: Optional[list] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    
    try:
        config = load_config(args.config)
        processor = WinnowerProcessor(config, args.model, args.verbose)
        
        processor.process(
            input_source=args.input,
            output_dir=args.output,
            recursive=args.recursive,
        )
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())