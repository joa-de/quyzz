import json
from pathlib import Path

imp

# Path to the default language file
LANGUAGE_FILE = "french.json"


class LanguageManager:
    """Manages the loading and retrieval of language strings."""

    def __init__(self, language_file=LANGUAGE_FILE):
        language_directory = Path(__file__).parent / "languages"
        self.language_file = language_directory / language_file
        self.strings = {}
        self.load_language()

    def load_language(self):
        """Load the language strings from the specified JSON file."""
        try:
            with open(self.language_file, "r", encoding="utf-8") as file:
                self.strings = json.load(file)
        except FileNotFoundError:
            print(
                f"\033[91mError: Language file '{self.language_file}' not found.\033[0m"
            )
            self.strings = {}
        except json.JSONDecodeError:
            print(
                f"\033[91mError: Language file '{self.language_file}' is not valid JSON.\033[0m"
            )
            self.strings = {}

    def get(self, key, default=""):
        """
        Retrieve a language string by key, with an optional default.
        Key can be in format "section.key" for nested strings.
        """
        if "." in key:
            section, subkey = key.split(".", 1)
            return self.strings.get(section, {}).get(subkey, default)
        else:
            # For backward compatibility, look in all sections
            for section in self.strings.values():
                if isinstance(section, dict) and key in section:
                    return section[key]
            return default
