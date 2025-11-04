"""Main CLI application entry point."""

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

from t3 import __version__
from t3.commands.init import init_app
from t3.commands.config import config_app

console = Console()

app = typer.Typer(
    name="t3",
    help="T3 CLI - A powerful command-line interface tool",
    rich_markup_mode="rich",
    add_completion=True,
)

# Add subcommands
app.add_typer(init_app, name="init")
app.add_typer(config_app, name="config")


def version_callback(value: bool) -> None:
    """Show version information."""
    if value:
        console.print(f"T3 CLI version: {__version__}", style="bold green")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """T3 CLI - A powerful command-line interface tool."""
    pass


@app.command()
def hello(
    name: str = typer.Option("World", "--name", "-n", help="Name to greet")
) -> None:
    """Say hello to someone."""
    console.print(f"Hello, [bold cyan]{name}[/bold cyan]! 👋", style="bold")


@app.command()
def status() -> None:
    """Show current system status."""
    table = Table(title="T3 CLI Status", show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Version", justify="right", style="blue")
    
    table.add_row("CLI", "✅ Active", __version__)
    table.add_row("Configuration", "✅ Loaded", "1.0")
    table.add_row("Database", "🟡 Connecting", "N/A")
    
    console.print(table)


if __name__ == "__main__":
    app()