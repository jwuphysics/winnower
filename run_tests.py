#!/usr/bin/env python3
"""
Test runner script for The Winnower.
Useful for CI/CD and local development.
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description or ' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    if result.returncode != 0:
        print(f"\n❌ FAILED: {description or ' '.join(cmd)}")
        return False
    else:
        print(f"\n✅ PASSED: {description or ' '.join(cmd)}")
        return True


def main():
    parser = argparse.ArgumentParser(description="Run tests for The Winnower")
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "smoke", "lint"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage",
        action="store_true", 
        help="Generate coverage report"
    )
    
    args = parser.parse_args()
    
    # Base pytest command
    pytest_cmd = ["python", "-m", "pytest"]
    if args.verbose:
        pytest_cmd.append("-v")
    if args.coverage:
        pytest_cmd.extend(["--cov=winnower", "--cov-report=html"])
    
    success = True
    
    if args.type in ["all", "smoke"]:
        success &= run_command(
            pytest_cmd + ["tests/test_smoke.py"],
            "Smoke tests (basic functionality)"
        )
    
    if args.type in ["all", "unit"]:
        success &= run_command(
            pytest_cmd + [
                "tests/test_config.py", 
                "tests/test_parsers.py", 
                "tests/test_cli.py"
            ],
            "Unit tests"
        )
    
    if args.type in ["all", "integration"]:
        success &= run_command(
            pytest_cmd + ["tests/test_integration.py"],
            "Integration tests"
        )
    
    if args.type in ["all", "lint"]:
        success &= run_command(
            ["python", "-m", "flake8", "winnower/", "tests/"],
            "Code linting with flake8"
        )
        success &= run_command(
            ["python", "-m", "black", "--check", "winnower/", "tests/"],
            "Code formatting check with black"
        )
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("💥 SOME TESTS FAILED!")
        return 1


if __name__ == "__main__":
    sys.exit(main())