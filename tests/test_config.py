"""Tests for core configuration manager."""

import json
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

from t3.core.config import ConfigManager


class TestConfigManager:
    """Test cases for ConfigManager class."""

    def test_init_with_default_path(self) -> None:
        """Test initialization with default config path."""
        with patch.object(ConfigManager, "load_config") as mock_load:
            config_manager = ConfigManager()
            expected_path = Path.home() / ".t3" / "config.json"
            assert config_manager.config_path == expected_path
            mock_load.assert_called_once()

    def test_init_with_custom_path(self) -> None:
        """Test initialization with custom config path."""
        custom_path = "/custom/path/config.json"
        with patch.object(ConfigManager, "load_config") as mock_load:
            config_manager = ConfigManager(custom_path)
            assert config_manager.config_path == Path(custom_path)
            mock_load.assert_called_once()

    @patch("pathlib.Path.exists")
    def test_load_config_file_not_exists(self, mock_exists: Mock) -> None:
        """Test loading config when file doesn't exist."""
        mock_exists.return_value = False
        config_manager = ConfigManager()
        assert config_manager._config_data == {}

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.open")
    def test_load_config_valid_file(
        self, mock_open_file: Mock, mock_exists: Mock
    ) -> None:
        """Test loading config from valid JSON file."""
        mock_exists.return_value = True
        test_data = {"key1": "value1", "key2": "value2"}

        mock_file = mock_open(read_data=json.dumps(test_data))
        mock_open_file.return_value = mock_file.return_value

        config_manager = ConfigManager()
        assert config_manager._config_data == test_data

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.open")
    def test_load_config_invalid_json(
        self, mock_open_file: Mock, mock_exists: Mock
    ) -> None:
        """Test loading config with invalid JSON."""
        mock_exists.return_value = True

        mock_file = mock_open(read_data="invalid json")
        mock_open_file.return_value = mock_file.return_value

        config_manager = ConfigManager()
        assert config_manager._config_data == {}

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.open")
    def test_save_config(self, mock_open_file: Mock, mock_mkdir: Mock) -> None:
        """Test saving config to file."""
        test_data = {"key": "value"}

        mock_file = mock_open()
        mock_open_file.return_value = mock_file.return_value

        config_manager = ConfigManager()
        config_manager._config_data = test_data
        config_manager.save_config()

        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_file.return_value.write.assert_called()

    def test_get_existing_key(self) -> None:
        """Test getting an existing configuration key."""
        config_manager = ConfigManager()
        config_manager._config_data = {"test_key": "test_value"}

        result = config_manager.get("test_key")
        assert result == "test_value"

    def test_get_non_existing_key(self) -> None:
        """Test getting a non-existing configuration key."""
        config_manager = ConfigManager()
        config_manager._config_data = {}

        result = config_manager.get("non_existing_key", "default")
        assert result == "default"

    @patch.object(ConfigManager, "save_config")
    def test_set_config(self, mock_save: Mock) -> None:
        """Test setting a configuration value."""
        config_manager = ConfigManager()

        config_manager.set("new_key", "new_value")

        assert config_manager._config_data["new_key"] == "new_value"
        mock_save.assert_called_once()

    @patch.object(ConfigManager, "save_config")
    def test_delete_existing_key(self, mock_save: Mock) -> None:
        """Test deleting an existing configuration key."""
        config_manager = ConfigManager()
        config_manager._config_data = {"key_to_delete": "value"}

        result = config_manager.delete("key_to_delete")

        assert result is True
        assert "key_to_delete" not in config_manager._config_data
        mock_save.assert_called_once()

    @patch.object(ConfigManager, "save_config")
    def test_delete_non_existing_key(self, mock_save: Mock) -> None:
        """Test deleting a non-existing configuration key."""
        config_manager = ConfigManager()
        config_manager._config_data = {}

        result = config_manager.delete("non_existing_key")

        assert result is False
        mock_save.assert_not_called()

    def test_get_all(self) -> None:
        """Test getting all configuration data."""
        test_data = {"key1": "value1", "key2": "value2"}
        config_manager = ConfigManager()
        config_manager._config_data = test_data

        result = config_manager.get_all()

        assert result == test_data
        assert result is not config_manager._config_data  # Should be a copy

    @patch("pathlib.Path.unlink")
    def test_reset(self, mock_unlink: Mock) -> None:
        """Test resetting configuration."""
        config_manager = ConfigManager()
        config_manager._config_data = {"key": "value"}

        config_manager.reset()

        assert config_manager._config_data == {}
        mock_unlink.assert_called_once_with(missing_ok=True)
