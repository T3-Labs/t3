"""Configuration management commands."""

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

console = Console()

config_app = typer.Typer(help="Configuration management")

CONFIG_FILE = Path.home() / ".t3" / "config.json"


@config_app.command()
def show() -> None:
    """Show current configuration."""
    config_data = _load_config()

    if not config_data:
        console.print("No configuration found", style="yellow")
        return

    table = Table(
        title="T3 CLI Configuration",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Key", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")

    for key, value in config_data.items():
        table.add_row(key, str(value))

    console.print(table)


@config_app.command()
def set(
    key: str = typer.Argument(..., help="Configuration key"),
    value: str = typer.Argument(..., help="Configuration value"),
) -> None:
    """Set a configuration value."""
    config_data = _load_config()
    config_data[key] = value
    _save_config(config_data)

    console.print(f"✅ Set {key} = {value}", style="green")


@config_app.command()
def get(
    key: str = typer.Argument(..., help="Configuration key"),
) -> None:
    """Get a configuration value."""
    config_data = _load_config()

    if key in config_data:
        console.print(f"{key} = {config_data[key]}", style="cyan")
    else:
        console.print(f"❌ Key '{key}' not found", style="red")
        raise typer.Exit(1)


@config_app.command()
def delete(
    key: str = typer.Argument(..., help="Configuration key"),
) -> None:
    """Delete a configuration value."""
    config_data = _load_config()

    if key in config_data:
        del config_data[key]
        _save_config(config_data)
        console.print(f"✅ Deleted '{key}'", style="green")
    else:
        console.print(f"❌ Key '{key}' not found", style="red")
        raise typer.Exit(1)


@config_app.command()
def reset() -> None:
    """Reset configuration to defaults."""
    from rich.prompt import Confirm

    if Confirm.ask("Are you sure you want to reset all configuration?"):
        CONFIG_FILE.unlink(missing_ok=True)
        console.print("✅ Configuration reset", style="green")
    else:
        console.print("❌ Reset cancelled", style="yellow")


def _load_config() -> dict:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        return {}

    try:
        with CONFIG_FILE.open("r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_config(config_data: dict) -> None:
    """Save configuration to file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CONFIG_FILE.open("w") as f:
        json.dump(config_data, f, indent=2)
