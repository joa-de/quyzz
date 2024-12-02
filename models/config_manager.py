import os
from pathlib import Path
import yaml
from typing import Any, Dict, Optional


class ConfigManager:
    """Model for managing application configuration."""

    def __init__(self, config_file: str = "config.yaml"):
        """
        Initialize ConfigManager with a specific config file.

        Args:
            config_file (str): Name of the config file to load
        """
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

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve a configuration value, supporting nested keys.

        Args:
            key (str): Dot-separated key path
            default (Any, optional): Value to return if key not found

        Returns:
            Configuration value or default
        """
        try:
            value = self._config
            for k in key.split("."):
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def get_all(self) -> Dict[str, Any]:
        """
        Get entire configuration dictionary.

        Returns:
            Full configuration dictionary
        """
        return self._config.copy()


def main():
    config = ConfigManager("config.yaml")
    key = "language_file"
    language_file = config.get(key)
    print(f" language file : {language_file}")


if __name__ == "__main__":
    main()
