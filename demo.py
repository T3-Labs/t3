#!/usr/bin/env python3
"""Example script demonstrating T3 CLI usage."""

import subprocess
import sys
from pathlib import Path


def run_cli_command(command: list) -> str:
    """Run a T3 CLI command and return the output."""
    try:
        result = subprocess.run(
            ["python", "-m", "t3.main"] + command,
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return ""


def main():
    """Demonstrate T3 CLI functionality."""
    print("🚀 T3 CLI Demo")
    print("=" * 50)

    # Show version
    print("\n📋 Version Information:")
    version_output = run_cli_command(["--version"])
    print(version_output)

    # Show status
    print("\n📊 System Status:")
    status_output = run_cli_command(["status"])
    print(status_output)

    # Configure settings
    print("\n🔧 Setting Configuration:")
    run_cli_command(["config", "set", "demo_setting", "example_value"])
    run_cli_command(["config", "set", "theme", "dark"])

    # Show configuration
    print("\n⚙️ Current Configuration:")
    config_output = run_cli_command(["config", "show"])
    print(config_output)

    # Create demo project
    print("\n📦 Creating Demo Project:")
    demo_path = Path("/tmp/t3-demo-project")
    if demo_path.exists():
        import shutil
        shutil.rmtree(demo_path)

    run_cli_command([
        "init", "project",
        "--name", "t3-demo-project",
        "--template", "python"
    ])

    print(f"✅ Demo project created at: {demo_path}")

    # List project contents
    if demo_path.exists():
        print("\n📁 Project Structure:")
        for item in demo_path.rglob("*"):
            if item.is_file():
                relative_path = item.relative_to(demo_path)
                print(f"   📄 {relative_path}")
            elif item.is_dir() and item != demo_path:
                relative_path = item.relative_to(demo_path)
                print(f"   📁 {relative_path}/")

    # Greet user
    print("\n👋 Greeting:")
    hello_output = run_cli_command(["hello", "--name", "T3 CLI User"])
    print(hello_output)

    print("\n🎉 Demo completed successfully!")
    print("💡 Try running the commands manually:")
    print("   python -m t3.main --help")
    print("   python -m t3.main status")
    print("   python -m t3.main config show")


if __name__ == "__main__":
    # Make sure we're in the right directory with virtual env
    project_root = Path(__file__).parent
    venv_path = project_root / ".venv" / "bin" / "activate"

    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run 'uv sync' first.")
        sys.exit(1)

    # Activate virtual environment and run demo
    main()
