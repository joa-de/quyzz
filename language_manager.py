import json
from pathlib import Path

# Path to the default language file
LANGUAGE_FILE = "french.json"


class LanguageManager:
    """Manages the loading and retrieval of language strings."""

    def __init__(self, language_file=LANGUAGE_FILE):
        self.language_directory = Path(__file__).parent / "languages"
        self.language_file = self.language_directory / language_file
        self.language = language_file.strip(".json")
        self.strings = {}
        self.load_language()
        if self.language != "dutch":
            self.load_translations()

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

    def load_translations(self):
        """
        Load translations from a file.

        Returns:
            dict: A dictionary mapping word IDs to  translations.
        """
        translations = {}
        filepath = self.language_directory
        filename = self.language + "-translations.txt"
        try:
            with open(filepath / filename, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("|")
                    if len(parts) == 2:
                        word_id = int(parts[0])
                        translations[word_id] = parts[1]
        except FileNotFoundError:
            print(f"Error: Translation file '{filename}' not found.")
            exit(1)
        except Exception as e:
            print(f"Error loading translations: {e}")
            exit(1)
        self.translations = translations
