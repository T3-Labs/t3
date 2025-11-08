"""Main CLI application entry point."""

import typer
from rich.console import Console
from rich.table import Table

from t3 import __version__
from t3.commands.config import config_app
from t3.commands.init import init_app

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


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """T3 CLI - A powerful command-line interface tool."""
    if ctx.invoked_subcommand is None:
        title_text = (
            "\n[bold cyan]T3 CLI[/bold cyan] - "
            "A powerful command-line interface tool\n"
        )
        console.print(title_text, style="bold")
        console.print(f"Version: [green]{__version__}[/green]\n")

        table = Table(
            title="Available Commands",
            show_header=True,
            header_style="bold magenta",
            border_style="cyan",
        )
        table.add_column("Command", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")

        table.add_row("hello", "Say hello to someone")
        table.add_row("status", "Show current system status")
        table.add_row("init project", "Initialize a new project with templates")
        table.add_row("init docker", "Initialize Docker environment with Edge Video")
        table.add_row("config show", "Show all configuration settings")
        table.add_row("config set", "Set a configuration value")
        table.add_row("config get", "Get a configuration value")
        table.add_row("config delete", "Delete a configuration key")
        table.add_row("config reset", "Reset configuration to defaults")

        console.print(table)
        console.print(
            "\n[yellow]💡 Tip:[/yellow] Use [cyan]t3 --help[/cyan] "
            "for detailed help"
        )
        tip_text = (
            "[yellow]💡 Tip:[/yellow] Use [cyan]t3 <command> --help[/cyan] "
            "for command-specific help\n"
        )
        console.print(tip_text)


@app.command()
def hello(
    name: str = typer.Option("World", "--name", "-n", help="Name to greet"),
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
