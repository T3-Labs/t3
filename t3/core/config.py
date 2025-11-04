"""Configuration handler for T3 CLI."""

import json
from pathlib import Path
from typing import Any, Dict


class ConfigManager:
    """
    A class to handle configuration management for T3 CLI.
    """

    def __init__(self, config_path: str | None = None) -> None:
        """
        Initialize the configuration manager.

        Args:
            config_path (str | None): Path to the configuration file.
                                     If None, uses default location.
        """
        self.config_path = (
            Path(config_path) if config_path
            else Path.home() / ".t3" / "config.json"
        )
        self._config_data: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file."""
        if not self.config_path.exists():
            self._config_data = {}
            return

        try:
            with self.config_path.open('r') as config_file:
                self._config_data = json.load(config_file)
        except (json.JSONDecodeError, OSError):
            self._config_data = {}

    def save_config(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with self.config_path.open('w') as config_file:
            json.dump(self._config_data, config_file, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key (str): The configuration key.
            default (Any): Default value if key not found.

        Returns:
            Any: The configuration value or default.
        """
        return self._config_data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value.

        Args:
            key (str): The configuration key.
            value (Any): The value to set.
        """
        self._config_data[key] = value
        self.save_config()

    def delete(self, key: str) -> bool:
        """
        Delete a configuration value.

        Args:
            key (str): The configuration key to delete.

        Returns:
            bool: True if key was deleted, False if key didn't exist.
        """
        if key in self._config_data:
            del self._config_data[key]
            self.save_config()
            return True
        return False

    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.

        Returns:
            Dict[str, Any]: All configuration data.
        """
        return self._config_data.copy()

    def reset(self) -> None:
        """Reset all configuration data."""
        self._config_data = {}
        self.config_path.unlink(missing_ok=True)