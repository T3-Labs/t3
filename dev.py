#!/usr/bin/env python3
"""Development script for T3 CLI."""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> None:
    """Run a command and print the result."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(
            command.split(),
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(f"Error: {e.stderr}")
        sys.exit(1)


def main():
    """Main development script."""
    if len(sys.argv) < 2:
        print("Usage: python dev.py [command]")
        print("\nAvailable commands:")
        print("  install    - Install development dependencies")
        print("  test       - Run tests")
        print("  lint       - Run linting")
        print("  format     - Format code")
        print("  build      - Build package")
        print("  clean      - Clean build artifacts")
        sys.exit(1)

    command = sys.argv[1]

    if command == "install":
        run_command("uv sync", "Installing dependencies")
        
    elif command == "test":
        run_command("pytest", "Running tests")
        
    elif command == "lint":
        run_command("ruff check .", "Running linter")
        
    elif command == "format":
        run_command("ruff format .", "Formatting code")
        
    elif command == "build":
        run_command("python -m build", "Building package")
        
    elif command == "clean":
        print("🔄 Cleaning build artifacts...")
        import shutil
        
        # Clean common build directories
        for dir_name in ["build", "dist", "*.egg-info"]:
            for path in Path(".").glob(dir_name):
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"Removed {path}")
        
        # Clean __pycache__ directories
        for path in Path(".").rglob("__pycache__"):
            shutil.rmtree(path)
            print(f"Removed {path}")
        
        print("✅ Clean completed")
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()