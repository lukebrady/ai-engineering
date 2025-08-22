#!/usr/bin/env python3
"""
Test runner script for the intro-langgraph project.

This script provides convenient ways to run tests with different configurations.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd: list[str]) -> int:
    """Run a command and return its exit code."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Run tests for intro-langgraph")
    parser.add_argument(
        "--coverage", 
        action="store_true", 
        help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true", 
        help="Run tests in verbose mode"
    )
    parser.add_argument(
        "--fast", 
        action="store_true", 
        help="Run tests in parallel for faster execution"
    )
    parser.add_argument(
        "--unit", 
        action="store_true", 
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration", 
        action="store_true", 
        help="Run only integration tests"
    )
    parser.add_argument(
        "--html", 
        action="store_true", 
        help="Generate HTML coverage report"
    )
    
    args = parser.parse_args()
    
    # Base command
    cmd = ["uv", "run", "pytest"]
    
    # Add test selection
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    else:
        cmd.append("tests/")
    
    # Add verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Add parallel execution
    if args.fast:
        cmd.extend(["-n", "auto"])
    
    # Add coverage
    if args.coverage:
        cmd.extend(["--cov=.", "--cov-report=term-missing"])
        if args.html:
            cmd.append("--cov-report=html")
    
    # Run the tests
    exit_code = run_command(cmd)
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
        if args.coverage and args.html:
            print("📊 HTML coverage report generated in htmlcov/")
    else:
        print(f"\n❌ Tests failed with exit code {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())