import os
from pathlib import Path
import yaml

# Description: Load config file
# Denis Joassin 2024


class config_manager:
    def __init__(self, config_file="config.yaml"):
        config_directory = Path(__file__).parent.parent / "config"
        self.config_file = config_directory / config_file
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load the config from the specified YAML file."""
        try:
            with open(self.config_file, "r", encoding="utf-8") as file:
                self.config = yaml.safe_load(file)
        except FileNotFoundError:
            print(f"\033[91mError: Config file '{self.config_file}' not found.\033[0m")
            self.config = {}
        except yaml.YAMLError:
            print(
                f"\033[91mError: Config file '{self.config_file}' is not valid YAML.\033[0m"
            )
            self.config = {}

    def get(self, key):
        """
        Retrieve a config value by key, with an optional default.
        Key can be in format "section.key" for nested values.
        """
        value = self.config
        value = value[key]
        return value


def main():
    config = config_manager("config.yaml")
    key = "language_file"
    language_file = config.get(key)
    print(f" language file : {language_file}")


if __name__ == "__main__":
    main()
