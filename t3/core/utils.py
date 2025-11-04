"""Utility functions for T3 CLI."""

import sys
from pathlib import Path
from typing import Any
from rich.console import Console
from rich.panel import Panel

console = Console()


def show_error(message: str) -> None:
    """
    Display an error message in a formatted panel.

    Args:
        message (str): The error message to display.
    """
    console.print(
        Panel(f"❌ {message}", title="Error", title_align="left", style="red")
    )


def show_success(message: str) -> None:
    """
    Display a success message in a formatted panel.

    Args:
        message (str): The success message to display.
    """
    console.print(
        Panel(f"✅ {message}", title="Success", title_align="left", style="green")
    )


def show_info(message: str) -> None:
    """
    Display an info message in a formatted panel.

    Args:
        message (str): The info message to display.
    """
    console.print(
        Panel(f"ℹ️ {message}", title="Info", title_align="left", style="blue")
    )


def show_warning(message: str) -> None:
    """
    Display a warning message in a formatted panel.

    Args:
        message (str): The warning message to display.
    """
    console.print(
        Panel(f"⚠️ {message}", title="Warning", title_align="left", style="yellow")
    )


def exit_with_error(message: str, code: int = 1) -> None:
    """
    Display an error message and exit with error code.

    Args:
        message (str): The error message to display.
        code (int): Exit code (default: 1).
    """
    show_error(message)
    sys.exit(code)


def validate_path(path: str, must_exist: bool = False) -> Path:
    """
    Validate and return a Path object.

    Args:
        path (str): Path string to validate.
        must_exist (bool): Whether the path must exist.

    Returns:
        Path: Validated Path object.

    Raises:
        ValueError: If path is invalid or doesn't exist when required.
    """
    path_obj = Path(path)

    if must_exist and not path_obj.exists():
        raise ValueError(f"Path does not exist: {path}")

    return path_obj


def format_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.

    Args:
        size_bytes (int): Size in bytes.

    Returns:
        str: Formatted size string.
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    size_index = 0
    size = float(size_bytes)

    while size >= 1024 and size_index < len(size_names) - 1:
        size /= 1024
        size_index += 1

    return f"{size:.1f} {size_names[size_index]}"


def is_valid_project_name(name: str) -> bool:
    """
    Check if a project name is valid.

    Args:
        name (str): Project name to validate.

    Returns:
        bool: True if name is valid, False otherwise.
    """
    if not name or len(name.strip()) == 0:
        return False

    # Check for invalid characters
    invalid_chars = set('/<>:"|?*\\')
    if any(char in invalid_chars for char in name):
        return False

    # Check if name is too long
    if len(name) > 255:
        return False

    return True