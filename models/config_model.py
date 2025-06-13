import os
from pathlib import Path
import yaml
from typing import Any, Dict, Optional


class ConfigModel:
    """Model for managing application configuration."""

    def __init__(self, config_file: str = None):
        """
        Initialize ConfigManager with a specific config file.

        Args:
            config_file (str): Name of the config file to load
        """
        if config_file is None:
            config_file = "config.yaml"

        self._config_directory = Path(__file__).parent.parent / "config"
        self._config_file = self._config_directory / config_file
        self._config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """
        Load configuration from YAML file.
        Raises exception on loading errors for caller to handle.
        """
        try:
            with open(self._config_file, "r", encoding="utf-8") as file:
                self._config = yaml.safe_load(file) or {}
        except (FileNotFoundError, yaml.YAMLError) as e:
            raise RuntimeError(f"Config file error: {e}")

    def get(self, key: str) -> Any:
        """
        Retrieve a configuration value, supporting nested keys.

        Args:
            key (str): Dot-separated key path

        """
        try:
            value = self._config[key]
            return value
        except KeyError:
            raise KeyError(f"Configuration key '{key}' not found.")

    def get_all(self) -> Dict[str, Any]:
        """
        Get entire configuration dictionary.

        Returns:
            Full configuration dictionary
        """
        return self._config.copy()


def main():
    config = ConfigModel("config.yaml")
    key = "language_file"
    language_file = config.get(key)
    print(f" language file : {language_file}")


if __name__ == "__main__":
    main()
