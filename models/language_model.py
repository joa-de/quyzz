import json
from pathlib import Path

# Path to the default language file
LANGUAGE_FILE = "french.json"


class LanguageModel:
    """Manages the loading and retrieval of language strings."""

    def __init__(self, language_file=LANGUAGE_FILE):
        self.language_directory = Path(__file__).parent.parent / "languages"
        self.language_file = self.language_directory / language_file
        self.language = language_file.strip(".json")
        self.strings = {}

        self._load_language()
        if self.language != "dutch":
            self._load_translations()

    def _load_language(self):
        """
        Attempt to load language strings from JSON file.
        Does not exit on error, allows caller to handle failures.
        """
        try:
            with open(self.language_file, "r", encoding="utf-8") as file:
                self.strings = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.strings = {}
            raise RuntimeError(f"Language file error: {e}")

    def _load_translations(self):
        """
        Load translations from a file.

        Raises:
            RuntimeError: If translation file cannot be loaded
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
            raise RuntimeError(f"Translation file '{filename}' not found")
        except Exception as e:
            raise RuntimeError(f"Error loading translations: {e}")

        self.translations = translations

    def get(self, key, default=""):
        """
        Retrieve a language string by key, supporting nested keys.

        Args:
            key (str): Key to retrieve, can be in 'section.subkey' format
            default (str): Fallback value if key is not found

        Returns:
            str: Retrieved language string or default
        """

        if "." in key:
            section, subkey = key.split(".", 1)
            return self.strings.get(section, {}).get(subkey, default)

        # Fallback search across all sections (For backward compatibility purpose)
        for section in self.strings.values():
            if isinstance(section, dict) and key in section:
                return section[key]

        return default

    def get_translation(self, word_id: int):
        """
        Retrieve a translation by word ID.

        Args:
            word_id (int): ID of the word to translate

        Returns:
            Optional[str]: Translation or None if not found
        """
        return self.translations.get(word_id)
